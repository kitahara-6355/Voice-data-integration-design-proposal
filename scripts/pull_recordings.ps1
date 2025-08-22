# PowerShell script to pull recordings from Pixel via adb
# Usage: Connect phone via USB (USB debugging ON) then run in PowerShell

$dest = Join-Path -Path (Get-Location) -ChildPath "storage/raw"
New-Item -ItemType Directory -Path $dest -Force | Out-Null

Write-Output "Listing adb devices..."
adb devices

# common recorder directories to try
$paths = @("/sdcard/Recorder", "/sdcard/Recordings", "/sdcard/Android/data/com.google.android.apps.recorder/files/Recordings", "/sdcard/Android/data/com.google.android.apps.recorder/files")

foreach ($p in $paths) {
    Write-Output "Checking $p"
    $exists = adb shell "[ -d '$p' ] && echo 'YES' || echo 'NO'" 2>$null
    if ($exists -match 'YES') {
        Write-Output "Pulling from $p"
        adb pull $p $dest | Out-Null
    }
}

# fallback: find media files under /sdcard
Write-Output "Performing fallback find (this may take a while)..."
adb shell "find /sdcard -type f \( -iname '*.m4a' -o -iname '*.wav' -o -iname '*.txt' -o -iname '*.pdf' \) 2>/dev/null" > .\scripts\phone_files.txt

Get-Content .\scripts\phone_files.txt | ForEach-Object {
    $f = $_.Trim()
    if ($f -ne "") {
        Write-Output "Pulling $f"
        adb pull "$f" $dest | Out-Null
    }
}

Write-Output "Pull complete. Files saved to $dest"
