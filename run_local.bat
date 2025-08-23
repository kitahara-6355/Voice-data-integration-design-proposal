@echo off
REM run_local.bat - For users who prefer double-click
IF NOT EXIST .venv (
  python -m venv .venv
)
call .venv\Scripts\activate.bat
start "" cmd /c ".venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 > uvicorn_stdout.log 2> uvicorn_stderr.log"
start "" cmd /c ".venv\Scripts\python.exe -m http.server 3000 -d frontend > frontend_stdout.log 2> frontend_stderr.log"
echo Backend: http://0.0.0.0:8000
echo Frontend: http://0.0.0.0:3000/index.html
pause
