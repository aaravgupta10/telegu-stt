@echo off
title Telugu TTS live demo
cd /d "%~dp0"
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
echo.
echo  Telugu text-to-speech demo
echo  --------------------------
echo  Starting. The first start takes about 1 to 2 minutes (the model is being loaded).
echo  When you see READY below, your browser opens by itself.
echo  If it does not, open this address in Chrome or Edge:  http://127.0.0.1:8000/
echo  To stop the demo, close this window.
echo.
"%~dp0python\python.exe" -I -X utf8 "%~dp0server.py" %*
echo.
echo  The demo has stopped. If this was not expected, take a photo of the text above.
pause
