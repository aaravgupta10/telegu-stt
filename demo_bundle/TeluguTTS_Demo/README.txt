TELUGU TEXT-TO-SPEECH: LIVE DEMO (runs on this laptop, no internet needed)
==========================================================================

WHAT THIS IS
  A prototype Telugu voice. You type a Telugu sentence in a web page and the model speaks it,
  on this laptop, without any cloud service. It is our fine-tuned version of Kyutai's Pocket TTS,
  trained on open Telugu speech data.

HOW TO START (about 2 minutes, do it BEFORE the meeting)
  1. Copy the whole folder "TeluguTTS_Demo" to the laptop (for example to the Desktop). Do not run it from a zip file:
     right-click the zip -> Extract All first.
  2. Double-click  START_DEMO.bat
  3. A black window opens and prints a few lines. Wait for the line that says  READY.
     (the first start takes 1 to 2 minutes while the model loads)
  4. Your browser opens by itself on  http://127.0.0.1:8000/
     If it does not, open Chrome or Edge and type that address.
  5. Click one of the example sentences (or paste Telugu text), choose a voice, press Speak.
  To stop: close the black window.

IF WINDOWS SHOWS A BLUE "WINDOWS PROTECTED YOUR PC" SCREEN
  Click "More info", then "Run anyway". (It appears because the program is not from the Microsoft store.)

IF THE FIREWALL ASKS FOR PERMISSION
  The demo only talks to this laptop itself (127.0.0.1). You may choose "Cancel" / "Block"; it still works.

WHAT TO EXPECT
  - A sentence of about 3 seconds of speech takes roughly 3 to 4 seconds to generate; a longer one (6 seconds) about 7.
    It is slower than a server because it runs on the laptop's processor. The black window prints the timing of each request.
  - Please do a test run with the sentences you plan to show BEFORE the meeting, and close other heavy programs.
  - Keep the laptop plugged in (battery saver mode makes it slower).

WHAT IT CAN AND CANNOT DO (please say this honestly in the meeting)
  - Telugu only. One sentence at a time (it splits your text at . ? !). End sentences with a full stop or question mark.
  - NUMBERS AND ENGLISH LETTERS ARE NOT SUPPORTED YET (the page will refuse them). Write numbers as Telugu words.
  - Up to 12 sentences per request; each sentence up to about 300 characters (long ones are split at commas automatically).
  - The voices come from open datasets (a male and a female studio speaker). Voice-consent and licensing questions are still
    being settled: please do not share or circulate the audio outside the meeting.
  - It is an early prototype: our automatic read-back test found the output about as recognisable as real recordings, but the tests were small.

SAFETY NET: PRE-RECORDED SAMPLES
  If the live demo does not start, open  recorded_samples\index.html  (double-click). It plays 20 sentences in two voices
  and two 30-second passages, all recorded earlier by this same model. It needs no setup.

TROUBLESHOOTING
  - "The demo has stopped" and the window shows red text: take a photo of the window and send it to the team.
  - The page says "Request failed" or nothing happens: look at the black window; if it is gone, start again with START_DEMO.bat.
  - Port 8000 already in use: start with  START_DEMO.bat --port 8001  (from a command prompt) and open http://127.0.0.1:8001/
  - If a message mentions a missing DLL (MSVCP140 or VCRUNTIME140): install "Microsoft Visual C++ Redistributable 2015-2022 (x64)"
    from Microsoft, then start again. (The needed files are already included, so this should not happen.)
  - Very slow (more than 3 times the audio length): close other programs, plug in the charger.

FOLDER CONTENTS
  START_DEMO.bat          starts everything
  server.py               the small web server (uses only this laptop)
  python\                 a private copy of Python and the libraries (nothing is installed on the laptop)
  files\model.safetensors the trained model (about 1.3 GB)
  files\tokenizer.json    the Telugu text tokenizer the model was trained with
  files\voices\           reference voices (any clean 5 to 10 second .wav placed here becomes a voice in the page)
  recorded_samples\       the pre-recorded fallback page
