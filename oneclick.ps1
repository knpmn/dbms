$projectDir = $PSScriptRoot
$url        = "http://localhost:8080"

Write-Host "--- HR Oracle Dashboard (Local) ---" -ForegroundColor Cyan

# Check if Docker Desktop is running
Write-Host "Checking Docker Desktop..." -ForegroundColor Yellow
$dockerRunning = $false
try {
    $result = docker info 2>&1
    if ($LASTEXITCODE -eq 0) {
        $dockerRunning = $true
    }
} catch { }

if (-not $dockerRunning) {
    Write-Host ""
    Write-Host "Docker Desktop is NOT running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Steps:" -ForegroundColor White
    Write-Host "  1. Open Docker Desktop from the Start Menu" -ForegroundColor White
    Write-Host "  2. Wait for it to finish starting up" -ForegroundColor White
    Write-Host "  3. Run this script again" -ForegroundColor White
    Write-Host ""

    $launch = Read-Host "Would you like to launch Docker Desktop now? (y/n)"
    if ($launch -eq 'y' -or $launch -eq 'Y') {
        Write-Host "Launching Docker Desktop..." -ForegroundColor Yellow
        $dockerDesktopPath = "$env:ProgramFiles\Docker\Docker\Docker Desktop.exe"
        if (Test-Path $dockerDesktopPath) {
            Start-Process $dockerDesktopPath
            Write-Host "Docker Desktop is starting. Wait for it to fully load, then run this script again." -ForegroundColor Green
        } else {
            Write-Host "Could not find Docker Desktop. Please launch it manually." -ForegroundColor Red
        }
    }

    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Docker Desktop is running." -ForegroundColor Green
Write-Host "Starting Docker containers..." -ForegroundColor Yellow
Set-Location $projectDir
docker compose up -d --build

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: docker compose failed to start the containers." -ForegroundColor Red
    Write-Host "Check the output above for details." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Waiting for server to start..." -ForegroundColor Yellow
$ready = $false
for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep -Seconds 1
    Write-Host "  Attempt $($i+1)/15..." -ForegroundColor DarkGray
    try {
        $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($resp.StatusCode -eq 200) { $ready = $true; break }
    } catch { }
}

if (-not $ready) {
    Write-Host ""
    Write-Host "WARNING: Server did not respond after 15 attempts." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Things to check:" -ForegroundColor White
    Write-Host "  1. Are you connected to the University VPN?" -ForegroundColor Cyan
    Write-Host "     The database requires VPN to be active." -ForegroundColor Cyan
    Write-Host "  2. Open your VPN client, connect, then run this script again." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  3. If VPN is already on, try opening $url manually." -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "Server is ready!" -ForegroundColor Green
}

Write-Host "LOCAL URL: $url" -ForegroundColor White
Start-Process $url

Read-Host "Press Enter to close this window"