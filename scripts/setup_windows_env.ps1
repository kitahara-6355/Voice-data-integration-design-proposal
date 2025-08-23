<#
setup_windows_env.ps1
Windows 向けの初期セットアップ支援スクリプト
実行: PowerShell で管理者でない通常ユーザで実行可
#>
Write-Output "=== setup_windows_env: start ==="

# 1) Python 確認
$py = & python -V 2>&1
if ($LASTEXITCODE -ne 0) {
  Write-Output "Python not found. Please install Python 3.10+ and ensure 'python' is in PATH."
  exit 1
} else {
  Write-Output "Python version: $py"
}

# 2) venv と依存
if (!(Test-Path ".venv")) {
  Write-Output "Creating virtual environment..."
  python -m venv .venv
}

Write-Output "Activating venv and installing requirements..."
. .\.venv\Scripts\Activate.ps1
pip install -U pip
pip install -r backend/requirements.txt

Write-Output "Checking ffmpeg availability..."
try {
    $ff = & ffmpeg -version 2>&1
    $firstLine = $ff | Select-Object -First 1
    Write-Output "ffmpeg found: $firstLine"
} catch {
    Write-Output "ffmpeg is not detected. Please install ffmpeg and add to PATH. See https://ffmpeg.org/download.html"
}

Write-Output "Setup finished. To run locally: .\run_local.ps1"
