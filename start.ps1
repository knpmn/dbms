# ─────────────────────────────────────────────────────────────────────────────
#  HR Oracle Dashboard — One-click startup script
#  Run: right-click → "Run with PowerShell"   OR   .\start.ps1 in terminal
# ─────────────────────────────────────────────────────────────────────────────

$projectDir = $PSScriptRoot
$url        = "http://localhost:8080"

Write-Host ""
Write-Host "============================" -ForegroundColor Cyan
Write-Host "  HR Oracle Dashboard" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Check Docker is running ───────────────────────────────────────────────
Write-Host "[1/3] Checking Docker..." -ForegroundColor Yellow
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Host "      Docker is running ✓" -ForegroundColor Green
} catch {
    Write-Host "      ERROR: Docker Desktop is not running." -ForegroundColor Red
    Write-Host "      Please start Docker Desktop and try again." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# ── 2. Build & start the container ──────────────────────────────────────────
Write-Host ""
Write-Host "[2/3] Starting container (building if needed)..." -ForegroundColor Yellow
Set-Location $projectDir
docker compose up -d --build

if ($LASTEXITCODE -ne 0) {
    Write-Host "      ERROR: docker compose failed. Check output above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "      Container started ✓" -ForegroundColor Green

# ── 3. Wait for Apache to be ready, then open browser ───────────────────────
Write-Host ""
Write-Host "[3/3] Waiting for the server to be ready..." -ForegroundColor Yellow
$ready = $false
for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep -Seconds 1
    try {
        $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($resp.StatusCode -eq 200) { $ready = $true; break }
    } catch {}
    Write-Host "      ..." -ForegroundColor DarkGray
}

if ($ready) {
    Write-Host "      Server is ready ✓" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Opening $url in your browser..." -ForegroundColor Cyan
    Start-Process $url
} else {
    Write-Host "      Server did not respond in time." -ForegroundColor Yellow
    Write-Host "      Try opening $url manually." -ForegroundColor Yellow
    Start-Process $url
}

Write-Host ""
Write-Host "  Dashboard: $url" -ForegroundColor Green
Write-Host "  To stop:   docker compose down" -ForegroundColor DarkGray
Write-Host ""
Read-Host "Press Enter to close this window"
