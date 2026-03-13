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
Write-Host "[2/5] Starting container..." -ForegroundColor Yellow
Set-Location $projectDir
docker compose up -d --build
if ($LASTEXITCODE -ne 0) {
    Write-Host "      ERROR: docker compose failed." -ForegroundColor Red
    Read-Host "Press Enter to exit"; exit 1
}

# 3. Check for Cloudflared tunnel executable
Write-Host "[3/5] Checking for cloudflared.exe..." -ForegroundColor Yellow
if (-not (Test-Path $cfExe)) {
    Write-Host "      cloudflared.exe not found! Downloading..." -ForegroundColor Cyan
    try {
        Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile $cfExe -UseBasicParsing
        Write-Host "      Download complete." -ForegroundColor Green
    } catch {
        Write-Host "      ERROR: Failed to download cloudflared.exe." -ForegroundColor Red
    }
} else {
    Write-Host "      cloudflared.exe is present." -ForegroundColor Green
}

# 4. Start Cloudflare Quick Tunnel
Write-Host "[4/5] Starting Cloudflare Quick Tunnel..." -ForegroundColor Yellow
if (Test-Path $cfExe) {
    # Starts the tunnel in a separate background process
    $cfProcess = Start-Process -FilePath $cfExe -ArgumentList "tunnel --url $url" -PassThru -WindowStyle Hidden
    Write-Host "      Tunnel process started (PID: $($cfProcess.Id))" -ForegroundColor Green
} else {
    Write-Host "      WARNING: cloudflared.exe not found in $projectDir" -ForegroundColor Red
}

# 5. Wait for Server & Finish
Write-Host "[5/5] Finalizing..." -ForegroundColor Yellow
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