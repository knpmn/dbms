$projectDir = $PSScriptRoot
$url        = "http://localhost:8080"
$cfExe      = Join-Path $projectDir "cloudflared.exe"

Write-Host "--- HR Oracle Dashboard (Cloudflare Tunnel) ---" -ForegroundColor Cyan

# 1. Check Docker
Write-Host "[1/4] Checking Docker..." -ForegroundColor Yellow
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Host "      Docker is running" -ForegroundColor Green
} catch {
    Write-Host "      ERROR: Docker Desktop is not running." -ForegroundColor Red
    Read-Host "Press Enter to exit"; exit 1
}

# 2. Build & Start Docker
Write-Host "[2/4] Starting container..." -ForegroundColor Yellow
Set-Location $projectDir
docker compose up -d --build
if ($LASTEXITCODE -ne 0) {
    Write-Host "      ERROR: docker compose failed." -ForegroundColor Red
    Read-Host "Press Enter to exit"; exit 1
}

# 3. Start Cloudflare Quick Tunnel
Write-Host "[3/4] Starting Cloudflare Quick Tunnel..." -ForegroundColor Yellow
if (Test-Path $cfExe) {
    # Starts the tunnel in a separate background process
    $cfProcess = Start-Process -FilePath $cfExe -ArgumentList "tunnel --url $url" -PassThru -WindowStyle Hidden
    Write-Host "      Tunnel process started (PID: $($cfProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "      WARNING: cloudflared.exe not found in $projectDir" -ForegroundColor Red
}

# 4. Wait for Server & Finish
Write-Host "[4/4] Finalizing..." -ForegroundColor Yellow
$ready = $false
for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep -Seconds 1
    try {
        $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($resp.StatusCode -eq 200) { $ready = $true; break }
    } catch { Write-Host "." -NoNewline }
}

Write-Host "`n"
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  LOCAL URL:  $url" -ForegroundColor Green
Write-Host "  REMOTE:     Check the cloudflared logs/output" -ForegroundColor Magenta
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  To stop the tunnel, close this window or use:"
Write-Host "  Stop-Process -Id $($cfProcess.Id)" -ForegroundColor DarkGray

# Open local browser
Start-Process $url

Read-Host "`nPress Enter to stop the tunnel and close this window"

# Cleanup: Kill the tunnel when the window is closed
if ($cfProcess) { Stop-Process -Id $cfProcess.Id -Force }