#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Live Telugu TTS demo: a tiny web page where you type a Telugu sentence and the model speaks it.

STATUS: written 2026-10-19. The web page and request handling were tested locally with a fake tone generator (--engine fake).
The real model path (--engine api, with --engine cli as the fallback) has NOT been run yet. Run it first on the notebook.

On the notebook (GPU, model loaded once):
  cd ~/SageMaker/tts/pocket-tts && source ~/SageMaker/tts/env.sh && \
  CUDA_VISIBLE_DEVICES=0 env -u LD_LIBRARY_PATH uv run python ~/SageMaker/tts/scripts/live_demo_server.py --device cuda --port 8000
Then open  https://<your-notebook-name>.notebook.us-east-1.sagemaker.aws/proxy/8000/   (the JupyterLab address with /lab replaced by /proxy/8000/).

Rules built in: one sentence at a time (text is split on . ? !), digits and Latin letters are refused (the model never saw them),
at most 12 sentences and 300 characters per sentence. The server listens on 127.0.0.1 only (not exposed to the internet).
"""
import argparse
import copy
import glob
import inspect
import io
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import unicodedata
import wave
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOME = os.path.expanduser("~/SageMaker/tts")
ZERO_WIDTH = {c: None for c in (0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF)}
BAD = re.compile("[0-9" + chr(0x0C66) + "-" + chr(0x0C6F) + "]|[A-Za-z]")
PAUSE_S = 0.30
MAX_SENTENCES, MAX_CHARS = 12, 300
LOCK = threading.Lock()


def clean_text(text):
    """The same rules as the training text cleaner (prep_syspin.py)."""
    t = unicodedata.normalize("NFC", text).translate(ZERO_WIDTH)
    for a, b in {"“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-", "…": "..."}.items():
        t = t.replace(a, b)
    t = t.replace(":", ",").replace(";", ",")
    t = re.sub(r"[\"'()\[\]{}]", "", t)
    t = re.sub(r"[-/\\|_*#~@^<>=+&%$]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+([,.?!])", r"\1", t)
    t = re.sub(r"([,.?!])\1+", r"\1", t)
    return t


def split_sentences(text):
    parts = [p.strip() for p in re.split(r"(?<=[.?!])\s+", text) if p.strip()]
    return [p if p[-1] in ".?!" else p + "." for p in parts]


def prepare(text):
    """Return (sentences, error_message)."""
    t = clean_text(text or "")
    if not t:
        return None, "Please type a Telugu sentence."
    if BAD.search(t):
        return None, "Numbers and English letters are not supported yet. Please write them in Telugu words or Telugu script."
    sents = split_sentences(t)
    if len(sents) > MAX_SENTENCES:
        return None, "Too long: please use at most %d sentences." % MAX_SENTENCES
    if any(len(s) > MAX_CHARS for s in sents):
        return None, "A sentence is too long (limit %d characters): please split it with . ? or !" % MAX_CHARS
    return sents, None


# ---------------------------------------------------------------- engines
def to_pcm(a):
    """float audio from the model -> raw 16-bit little-endian PCM bytes (numpy is available on the notebook)."""
    import numpy as np
    a = np.asarray(a, dtype="float32").reshape(-1)
    return (np.clip(a, -1.0, 1.0) * 32767.0).astype("<i2").tobytes()


class FakeEngine:
    """For testing the page: a short tone per sentence, length proportional to the text."""
    sr = 24000

    def synth(self, text, voice_path):
        import array
        secs = max(0.8, len(text) / 14.0)
        f = 220.0 if "_f_" in voice_path or "female" in voice_path else 140.0
        a = array.array("h", (int(9000 * math.sin(2 * math.pi * f * i / self.sr) * (0.6 + 0.4 * math.sin(2 * math.pi * 3 * i / self.sr)))
                              for i in range(int(self.sr * secs))))
        return a.tobytes()


class ApiEngine:
    """Loads the model once with Kyutai's Python interface (documented, not yet run by us)."""

    def __init__(self, cfg, ckpt, device):
        from pocket_tts import TTSModel
        sig = inspect.signature(TTSModel.load_model)
        print("TTSModel.load_model signature:", sig, flush=True)
        kw = {"config": cfg, "checkpoint": ckpt}
        if "device" in sig.parameters:
            kw["device"] = device
        elif device != "cpu":
            print("WARNING: load_model has no device argument; the model may run on the CPU.", flush=True)
        self.model = TTSModel.load_model(**kw)
        self.sr = int(self.model.sample_rate)

    def synth(self, text, voice_path):
        # recompute the voice state for each sentence: cheap (about 0.3 s) and safe if the state is consumed by generation
        state = self.model.get_state_for_audio_prompt(voice_path)
        audio = self.model.generate_audio(state, text)
        try:
            audio = audio.detach().cpu().numpy()
        except AttributeError:
            pass
        return to_pcm(audio)


class CliEngine:
    """Fallback: one 'pocket-tts generate' process per sentence (about 14 s each, model reloaded every time)."""
    sr = 24000

    def __init__(self, cfg, ckpt, device):
        self.cfg, self.ckpt, self.device = cfg, ckpt, device

    def synth(self, text, voice_path):
        out = tempfile.mktemp(suffix=".wav")
        cmd = ["pocket-tts", "generate", "--config", self.cfg, "--checkpoint", self.ckpt, "--voice", voice_path,
               "--text", text, "--output-path", out, "--device", self.device, "-q"]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(out):
            raise RuntimeError("pocket-tts generate failed: " + r.stderr[-300:])
        with wave.open(out) as w:
            a = w.readframes(w.getnframes())
        os.remove(out)
        return a


def make_cfg(tokenizer_json, out_path):
    import yaml
    c = yaml.safe_load(open("pocket_tts/config/english_2026-04_24l.yaml"))
    c["flow_lm"]["lookup_table"]["tokenizer_path"] = tokenizer_json
    yaml.safe_dump(c, open(out_path, "w"), sort_keys=False)
    return out_path


def wav_bytes(chunks, sr):
    """chunks: list of raw 16-bit PCM bytes, one per sentence; joined with a short silence."""
    gap = b"\x00\x00" * int(sr * PAUSE_S)
    data = gap.join(chunks)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(data)
    return buf.getvalue(), len(data) / 2 / sr


# ---------------------------------------------------------------- web page
PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Telugu TTS live demo</title>
<style>
:root{--bg:#fff;--fg:#1a1a1a;--mut:#666;--line:#ddd;--card:#f7f7f8;--acc:#1f5eff}
@media (prefers-color-scheme:dark){:root{--bg:#161618;--fg:#eee;--mut:#9a9a9a;--line:#333;--card:#202023;--acc:#6b95ff}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,"Segoe UI","Nirmala UI",sans-serif}
main{max-width:760px;margin:0 auto;padding:24px 16px 48px}h1{font-size:1.4rem;margin:0 0 4px}.sub{color:var(--mut);margin:0 0 14px}
textarea{width:100%;box-sizing:border-box;min-height:120px;font:1.25rem/1.5 system-ui,"Nirmala UI",sans-serif;padding:10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg)}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:12px 0}select,button{font:inherit;padding:8px 14px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--fg)}
button.go{background:var(--acc);color:#fff;border-color:var(--acc);font-weight:600;cursor:pointer}button:disabled{opacity:.55}
.ex button{margin:3px 4px 3px 0;font-size:1rem;cursor:pointer}#st{color:var(--mut);min-height:1.4em}#err{color:#c0392b;font-weight:600}
audio{width:100%;margin-top:10px}.note{font-size:.85rem;color:var(--mut);margin-top:22px}
</style></head><body><main>
<h1>Telugu text-to-speech: live demo</h1>
<p class="sub">Type a Telugu sentence and press Speak. The model generates the audio on the spot.</p>
<textarea id="t" lang="te" placeholder="Type or paste Telugu text here"></textarea>
<div class="row"><select id="v">__VOICES__</select><button class="go" id="b" onclick="speak()">Speak</button><span id="st"></span></div>
<div id="err"></div>
<audio id="a" controls></audio>
<div class="ex"><div class="sub" style="margin:14px 0 4px">Examples (tap to fill):</div>__EXAMPLES__</div>
<p class="note">Prototype. One sentence at a time; end sentences with . ? or !. Numbers and English letters are not supported yet. Voices come from open-dataset speakers and are for internal demonstration only.</p>
</main>
<script>
function ex(s){document.getElementById('t').value=s}
async function speak(){
  const b=document.getElementById('b'),st=document.getElementById('st'),er=document.getElementById('err'),a=document.getElementById('a');
  er.textContent='';const text=document.getElementById('t').value;if(!text.trim()){er.textContent='Please type a Telugu sentence.';return}
  b.disabled=true;st.textContent='Generating...';const t0=performance.now();
  try{
    const r=await fetch('tts',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:text,voice:document.getElementById('v').value})});
    if(!r.ok){let m='Error';try{m=(await r.json()).error}catch(e){}er.textContent=m;st.textContent='';return}
    const blob=await r.blob();a.src=URL.createObjectURL(blob);a.play().catch(()=>{});
    st.textContent='Done: '+r.headers.get('X-Audio-Seconds')+' s of audio, '+((performance.now()-t0)/1000).toFixed(1)+' s total';
  }catch(e){er.textContent='Request failed: '+e}finally{b.disabled=false}
}
document.getElementById('t').addEventListener('keydown',function(e){if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)){speak()}});
</script></body></html>"""

EXAMPLES = ["మీ పేరు ఏమిటి?",
            "నమస్కారం, మీరు ఎలా ఉన్నారు?",
            "ఈ రోజు వాతావరణం చాలా చల్లగా ఉంది.",
            "నేను రేపు విజయవాడ వెళ్తున్నాను.",
            "దయచేసి ఒక్క నిమిషం వేచి ఉండండి."]


def find_voices(args):
    v = {}
    if os.path.exists(args.female):
        v["female_a"] = ("Female A (studio, evaluated)", args.female)
    if args.female_b is None:
        for p in sorted(glob.glob(HOME + "/data/full_Rasa/wavs/TEL_F_*.wav")):
            try:
                with wave.open(p) as w:
                    d = w.getnframes() / w.getframerate()
                if w.getframerate() == 24000 and 4.0 <= d <= 9.0:
                    args.female_b = p
                    break
            except Exception:
                continue
    if args.female_b and os.path.exists(args.female_b):
        v["female_b"] = ("Female B (different speaker, not evaluated)", args.female_b)
    if os.path.exists(args.male):
        v["male"] = ("Male (studio, evaluated)", args.male)
    if args.engine == "fake" and not v:
        v = {"female_a": ("Female A (test tone)", "x_f_test.wav"), "male": ("Male (test tone)", "x_m_test.wav")}
    return v


def make_handler(engine, voices):
    import html as _h
    opts = "".join('<option value="%s">%s</option>' % (k, _h.escape(lbl)) for k, (lbl, _) in voices.items())
    exs = "".join('<button type="button" lang="te" onclick="ex(this.dataset.t)" data-t="%s">%s</button>' % (_h.escape(e, quote=True), _h.escape(e)) for e in EXAMPLES)
    page = PAGE.replace("__VOICES__", opts).replace("__EXAMPLES__", exs).encode("utf-8")

    class H(BaseHTTPRequestHandler):
        def log_message(self, fmt, *a):
            sys.stderr.write("%s %s\n" % (time.strftime("%H:%M:%S"), fmt % a))

        def _send(self, code, body, ctype, extra=None):
            self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(body)))
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers(); self.wfile.write(body)

        def do_GET(self):
            if self.path.rstrip("/").endswith("health"):
                self._send(200, json.dumps({"ok": True, "voices": list(voices)}).encode(), "application/json")
            else:
                self._send(200, page, "text/html; charset=utf-8")

        def do_POST(self):
            try:
                n = int(self.headers.get("Content-Length", "0"))
                req = json.loads(self.rfile.read(n).decode("utf-8"))
                sents, err = prepare(req.get("text", ""))
                if err:
                    return self._send(400, json.dumps({"error": err}).encode(), "application/json")
                vk = req.get("voice") if req.get("voice") in voices else next(iter(voices))
                t0 = time.time(); chunks = []
                with LOCK:
                    for s in sents:
                        chunks.append(engine.synth(s, voices[vk][1]))
                body, secs = wav_bytes(chunks, engine.sr)
                sys.stderr.write("%s TTS %d sentence(s), %.1f s audio in %.1f s (voice %s)\n" % (time.strftime("%H:%M:%S"), len(sents), secs, time.time() - t0, vk))
                self._send(200, body, "audio/wav", {"X-Audio-Seconds": "%.1f" % secs})
            except Exception as e:
                traceback.print_exc()
                self._send(500, json.dumps({"error": "Generation failed: %s" % e}).encode(), "application/json")
    return H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default="api", choices=["api", "cli", "fake"])
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--checkpoint", default=HOME + "/runs/telugu_full/checkpoint_00015000.pt")
    ap.add_argument("--tokenizer", default=HOME + "/data/full/tokenizer.json")
    ap.add_argument("--female", default=HOME + "/data/full_Female/wavs/IISc_SYSPINProject_te_f_AGRI_00216.wav")
    ap.add_argument("--female-b", default=None, dest="female_b")
    ap.add_argument("--male", default=HOME + "/data/full_Male/wavs/IISc_SYSPINProject_te_m_BOOK_10500.wav")
    args = ap.parse_args()

    voices = find_voices(args)
    if not voices:
        sys.exit("No reference voice files found. Check --female / --male paths.")
    print("voices:", {k: v[1] for k, v in voices.items()}, flush=True)
    if args.engine == "fake":
        engine = FakeEngine()
    else:
        cfg = make_cfg(os.path.expanduser(args.tokenizer), HOME + "/live_demo_gen.yaml")
        ckpt = os.path.expanduser(args.checkpoint)
        engine = None
        if args.engine == "api":
            try:
                t0 = time.time(); engine = ApiEngine(cfg, ckpt, args.device)
                print("model loaded through the Python interface in %.1f s" % (time.time() - t0), flush=True)
            except Exception:
                traceback.print_exc(); print("Python interface failed; falling back to the command-line engine (slower).", flush=True)
        if engine is None:
            engine = CliEngine(cfg, ckpt, args.device)
        # warm-up so the first request is fast
        try:
            t0 = time.time(); first = next(iter(voices.values()))[1]
            engine.synth(EXAMPLES[0], first); print("warm-up sentence done in %.1f s" % (time.time() - t0), flush=True)
        except Exception:
            traceback.print_exc(); print("WARNING: warm-up failed; the first request may fail too.", flush=True)
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(engine, voices))
    print("READY on http://127.0.0.1:%d/ (engine %s)" % (args.port, type(engine).__name__), flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
