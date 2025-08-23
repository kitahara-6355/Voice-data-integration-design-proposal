<#
run_local.ps1
目的: Windows 環境で Docker を使わずにバックエンド（FastAPI）とフロント（静的）を立ち上げる
使い方:
  1) PowerShell 管理者ではない通常ユーザーで実行可能
  2) プロジェクトルートで: .\run_local.ps1
#>

param(
  [string]$HOST = "0.0.0.0",
  [int]$BACKEND_PORT = 8000,
  [int]$FRONTEND_PORT = 3000
)

Write-Output "=== run_local: starting ==="
if (!(Test-Path ".venv")) {
    Write-Output "No venv found. Creating .venv..."
    python -m venv .venv
}

Write-Output "Activating venv..."
. .\.venv\Scripts\Activate.ps1

Write-Output "Ensuring required directories..."
if (!(Test-Path -Path "./storage/processed")) { New-Item -ItemType Directory -Path "./storage/processed" | Out-Null }
if (!(Test-Path -Path "./chroma_db")) { New-Item -ItemType Directory -Path "./chroma_db" | Out-Null }
if (!(Test-Path -Path "./hf_cache")) { New-Item -ItemType Directory -Path "./hf_cache" | Out-Null }

Write-Output "Starting backend (uvicorn) -> logs: uvicorn_stdout.log / uvicorn_stderr.log"
# Start uvicorn in separate process and redirect output
Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m uvicorn backend.app.main:app --host $HOST --port $BACKEND_PORT" -NoNewWindow -RedirectStandardOutput "./uvicorn_stdout.log" -RedirectStandardError "./uvicorn_stderr.log"

Start-Sleep -Seconds 2

Write-Output "Starting simple static server for frontend -> logs: frontend_stdout.log / frontend_stderr.log"
# Use Python's http.server to serve frontend directory
Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m http.server $FRONTEND_PORT -d frontend" -NoNewWindow -RedirectStandardOutput "./frontend_stdout.log" -RedirectStandardError "./frontend_stderr.log"

Write-Output "Local servers started."
Write-Output "Backend: http://$HOST`:$BACKEND_PORT (health: /api/health)"
Write-Output "Frontend: http://$HOST`:$FRONTEND_PORT/index.html"
Write-Output "Logs are in project root: uvicorn_*.log frontend_*.log"
