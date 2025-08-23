# run_local.ps1 (project root)
# This script starts the backend server. The frontend is served by the same server.

# Set PowerShell to stop on errors.
$ErrorActionPreference = "Stop"

Write-Output "Ensuring virtual environment exists..."
if (!(Test-Path -Path ".\.venv")) {
    Write-Output "Virtual environment not found. Please run the following commands first:"
    Write-Output "python -m venv .venv"
    Write-Output ".\.venv\Scripts\Activate.ps1"
    Write-Output "pip install -r backend\requirements.txt"
    exit 1
}

Write-Output "Starting backend server in the background..."
Write-Output "Logs will be written to uvicorn_stdout.log and uvicorn_stderr.log"

# Define arguments for the process
$arguments = "-m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --loop asyncio"

# Start the process. Note: This will run in the background. The script will exit,
# but the server process will keep running.
Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList $arguments -NoNewWindow -RedirectStandardOutput "./uvicorn_stdout.log" -RedirectStandardError "./uvicorn_stderr.log"

Write-Output ""
Write-Output "✅ Server process started in the background."
Write-Output "   You can access the application at http://localhost:8000"
Write-Output "   To stop the server, you may need to find and stop the 'python.exe' process in Task Manager."
