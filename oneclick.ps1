$projectDir = $PSScriptRoot
$url        = "http://localhost:8080"

Write-Host "--- HR Oracle Dashboard (Local) ---" -ForegroundColor Cyan

Write-Host "Starting Docker containers..." -ForegroundColor Yellow
Set-Location $projectDir
docker compose up -d --build
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: docker compose failed." -ForegroundColor Red
    Read-Host "Press Enter to exit"; exit 1
}

Write-Host "Waiting for server to start..." -ForegroundColor Yellow
$ready = $false
for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep -Seconds 1
    try {
        $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($resp.StatusCode -eq 200) { $ready = $true; break }
    } catch { }
}

Write-Host "`nServer is ready!" -ForegroundColor Green
Write-Host "LOCAL URL: $url" -ForegroundColor White

Start-Process $url

Read-Host "`nPress Enter to close this window"