#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Telugu TTS live demo, portable version: runs on a normal laptop (CPU), fully offline.

Type a Telugu sentence in the web page, pick a voice, press Speak, and the model speaks it.
Everything it needs is in the folder `files/` next to this script:
  files/model.safetensors   the fine-tuned model (exported at step 15,000)
  files/tokenizer.json      the Telugu tokenizer used in training
  files/voices/*.wav        reference voices (5-10 s of clean speech each); the file name becomes the voice name
No internet, no Hugging Face login and no AWS are needed. The page only listens on this computer (127.0.0.1).

STATUS: written 2026-10-19. The web page and request handling were tested with a fake tone generator (--engine fake).
The real-model path (default) is tested on the first run with the real files; read the console output.

Rules built in: one sentence at a time (text is split on . ? !), digits and Latin letters are refused (the model never saw them),
at most 12 sentences and 300 characters per sentence.
"""
import argparse
import io
import json
import math
import os
import re
import sys
import threading
import time
import traceback
import unicodedata
import wave
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILES = HERE / "files"
ZERO_WIDTH = {c: None for c in (0x200B, 0x200C, 0x200D, 0x2060, 0xFEFF)}
BAD = re.compile("[0-9" + chr(0x0C66) + "-" + chr(0x0C6F) + "]|[A-Za-z]")
PAUSE_S = 0.30
MAX_SENTENCES, MAX_CHARS = 12, 300
LOCK = threading.Lock()


def clean_text(text):
    """The same rules as the training text cleaner (prep_syspin.py)."""
    t = unicodedata.normalize("NFC", text).translate(ZERO_WIDTH)
    for a, b in {0x201C: '"', 0x201D: '"', 0x2018: "'", 0x2019: "'", 0x2013: "-", 0x2014: "-", 0x2026: "..."}.items():
        t = t.replace(chr(a), b)
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


# ---------------------------------------------------------------- engines (they return raw 16-bit PCM bytes)
def to_pcm(a):
    import numpy as np
    a = np.asarray(a, dtype="float32").reshape(-1)
    return (np.clip(a, -1.0, 1.0) * 32767.0).astype("<i2").tobytes()


class FakeEngine:
    """For testing the page only: a short tone per sentence."""
    sr = 24000

    def synth(self, text, voice_path):
        import array
        secs = max(0.8, len(text) / 14.0)
        f = 220.0 if "female" in os.path.basename(voice_path).lower() else 140.0
        return array.array("h", (int(9000 * math.sin(2 * math.pi * f * i / self.sr) * (0.6 + 0.4 * math.sin(2 * math.pi * 3 * i / self.sr)))
                                 for i in range(int(self.sr * secs)))).tobytes()


class RealEngine:
    """Loads our fine-tuned model once, from local files only (Kyutai's own loading code)."""

    def __init__(self, quantize=False, threads=0):
        import torch
        import yaml
        import pocket_tts
        from pocket_tts import TTSModel
        if not threads:    # batch-size-1 generation gains little beyond a handful of threads; avoid both 1 and "all"
            threads = min(8, max(2, (os.cpu_count() or 4) // 2))
        torch.set_num_threads(threads)
        print("PyTorch CPU threads:", torch.get_num_threads(), flush=True)
        w, tok = FILES / "model.safetensors", FILES / "tokenizer.json"
        for p in (w, tok):
            if not p.exists():
                raise FileNotFoundError("missing file: %s" % p)
        base = Path(pocket_tts.__file__).parent / "config" / "english_2026-04_24l.yaml"
        cfg = yaml.safe_load(open(base, encoding="utf-8"))
        cfg["weights_path"] = str(w.resolve())
        cfg["weights_path_without_voice_cloning"] = str(w.resolve())
        cfg["flow_lm"]["lookup_table"]["tokenizer_path"] = str(tok.resolve())
        cfg_path = FILES / "gen_local.yaml"
        yaml.safe_dump(cfg, open(cfg_path, "w", encoding="utf-8"), sort_keys=False)
        self.model = TTSModel.load_model(config=str(cfg_path), quantize=quantize)
        self.sr = int(self.model.sample_rate)
        self.states = {}
        print("voice cloning available:", getattr(self.model, "has_voice_cloning", "unknown"), flush=True)

    def synth(self, text, voice_path):
        if voice_path not in self.states:
            self.states[voice_path] = self.model.get_state_for_audio_prompt(voice_path)
        audio = self.model.generate_audio(self.states[voice_path], text)   # copy_state=True: the cached voice state is kept intact
        return to_pcm(audio.detach().cpu().numpy())


PAUSE_COMMA_S = 0.15
TOKEN_LIMIT = 45          # Kyutai warns that chunks over 50 tokens "may skip words"; stay safely below
CHUNKER = None


class Chunker:
    """Splits a long sentence at commas into pieces of at most TOKEN_LIMIT tokens of OUR tokenizer."""

    def __init__(self, tok_path):
        from tokenizers import Tokenizer
        self.tok = Tokenizer.from_file(str(tok_path))

    def n(self, s):
        return len(self.tok.encode(s).ids)

    def chunks(self, sentence, limit=TOKEN_LIMIT):
        if self.n(sentence) <= limit:
            return [sentence]
        parts = [p.strip() for p in re.split(r"(?<=,)\s+", sentence) if p.strip()]
        out, cur = [], ""
        for p in parts:
            cand = (cur + " " + p).strip() if cur else p
            if cur and self.n(cand) > limit:
                out.append(cur); cur = p
            else:
                cur = cand
        if cur:
            out.append(cur)
        return out


def wav_bytes(pieces, sr):
    """pieces: list of (raw 16-bit PCM bytes, silence in seconds before it); the first silence is ignored."""
    data = b""
    for i, (pcm, gap_s) in enumerate(pieces):
        if i:
            data += b"\x00\x00" * int(sr * gap_s)
        data += pcm
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
<p class="sub">Type a Telugu sentence and press Speak. The model generates the audio on this computer.</p>
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
    st.textContent='Done: '+r.headers.get('X-Audio-Seconds')+' s of audio in '+((performance.now()-t0)/1000).toFixed(1)+' s';
  }catch(e){er.textContent='Request failed: '+e}finally{b.disabled=false}
}
document.getElementById('t').addEventListener('keydown',function(e){if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)){speak()}});
</script></body></html>"""

EXAMPLES = ["మీ పేరు ఏమిటి?",
            "నమస్కారం, మీరు ఎలా ఉన్నారు?",
            "ఈ రోజు వాతావరణం చాలా చల్లగా ఉంది.",
            "నేను రేపు విజయవాడ వెళ్తున్నాను.",
            "దయచేసి ఒక్క నిమిషం వేచి ఉండండి."]


def find_voices(engine_name):
    voices = {}
    for p in sorted((FILES / "voices").glob("*.wav")):
        voices[p.stem] = (p.stem.replace("_", " ").title(), str(p))
    if not voices and engine_name == "fake":
        voices = {"female_test": ("Female (test tone)", "female_test.wav"), "male_test": ("Male (test tone)", "male_test.wav")}
    return voices


def make_handler(engine, voices):
    import html as _h
    opts = "".join('<option value="%s">%s</option>' % (_h.escape(k, quote=True), _h.escape(lbl)) for k, (lbl, _) in voices.items())
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
                t0 = time.time(); pieces = []
                with LOCK:
                    for s in sents:
                        parts = CHUNKER.chunks(s) if CHUNKER else [s]
                        for k, part in enumerate(parts):
                            pieces.append((engine.synth(part, voices[vk][1]), PAUSE_S if k == 0 else PAUSE_COMMA_S))
                body, secs = wav_bytes(pieces, engine.sr)
                sys.stderr.write("%s TTS %d sentence(s) in %d piece(s), %.1f s audio in %.1f s (voice %s)\n" % (time.strftime("%H:%M:%S"), len(sents), len(pieces), secs, time.time() - t0, vk))
                self._send(200, body, "audio/wav", {"X-Audio-Seconds": "%.1f" % secs})
            except Exception as e:
                traceback.print_exc()
                self._send(500, json.dumps({"error": "Generation failed: %s" % e}).encode(), "application/json")
    return H


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", default="real", choices=["real", "fake"])
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--quantize", action="store_true", help="int8 speed-up (Kyutai option; quality not yet checked on our model)")
    ap.add_argument("--threads", type=int, default=0, help="CPU threads for PyTorch (0 = default)")
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    global CHUNKER
    if (FILES / "tokenizer.json").exists():
        try:
            CHUNKER = Chunker(FILES / "tokenizer.json")
            print("tokenizer loaded for the long-sentence guard (limit %d tokens per piece)" % TOKEN_LIMIT, flush=True)
        except Exception:
            traceback.print_exc(); print("WARNING: could not load tokenizer.json for the guard.", flush=True)
    voices = find_voices(args.engine)
    if not voices:
        sys.exit("No reference voices found: put 5-10 s .wav files into %s" % (FILES / "voices"))
    print("voices:", ", ".join(voices), flush=True)
    t0 = time.time()
    engine = FakeEngine() if args.engine == "fake" else RealEngine(args.quantize, args.threads)
    print("model loaded in %.1f s" % (time.time() - t0), flush=True)
    try:   # warm-up so the first request is fast, and to catch problems before the demo starts
        t0 = time.time(); engine.synth(EXAMPLES[0], next(iter(voices.values()))[1])
        print("warm-up sentence done in %.1f s" % (time.time() - t0), flush=True)
    except Exception:
        traceback.print_exc(); print("WARNING: warm-up failed; the first request may fail too.", flush=True)
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(engine, voices))
    url = "http://127.0.0.1:%d/" % args.port
    print("READY: open %s (it opens automatically). Press Ctrl+C in this window to stop." % url, flush=True)
    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    srv.serve_forever()


if __name__ == "__main__":
    main()
