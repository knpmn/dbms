$projectDir = $PSScriptRoot
$url        = "http://localhost:8080"
$cfExe      = Join-Path $projectDir "cloudflared.exe"
$tempLog    = Join-Path $projectDir "cf_tunnel.log"

Write-Host "--- HR Oracle Dashboard ---" -ForegroundColor Cyan

# 1. Start Docker (Simplified check)
Write-Host "[1/3] Starting Docker containers..." -ForegroundColor Yellow
Set-Location $projectDir
docker compose up -d --build
if ($LASTEXITCODE -ne 0) { Write-Host "Docker failed!" -ForegroundColor Red; exit 1 }

# 2. Start Tunnel and Capture URL
Write-Host "[2/3] Generating Cloudflare URL..." -ForegroundColor Yellow
if (Test-Path $cfExe) {
    # Start tunnel and redirect output to a temp log file
    Start-Process -FilePath $cfExe -ArgumentList "tunnel --url $url" -RedirectStandardError $tempLog -WindowStyle Hidden
    
    # Wait for the URL to appear in the log file
    $foundUrl = $null
    for ($i = 0; $i -lt 10; $i++) {
        Start-Sleep -Seconds 1
        if (Test-Path $tempLog) {
            $content = Get-Content $tempLog
            $line = $content | Select-String "https://.*\.trycloudflare\.com"
            if ($line) {
                $foundUrl = $line.Matches.Value
                break
            }
        }
    }
}

# 3. Display Results
Write-Host "[3/3] System Ready!" -ForegroundColor Green
Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  LOCAL ACCESS:  $url" -ForegroundColor White
if ($foundUrl) {
    Write-Host "  PUBLIC LINK:   $foundUrl" -ForegroundColor Magenta
    # Optionally open the public link automatically:
    # Start-Process $foundUrl
} else {
    Write-Host "  PUBLIC LINK:   Timed out. Check cf_tunnel.log" -ForegroundColor Red
}
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Open local site automatically
Start-Process $url

Read-Host "Press Enter to STOP tunnel and exit"

# Cleanup: Kill cloudflared and delete log
Get-Process cloudflared -ErrorAction SilentlyContinue | Stop-Process -Force
if (Test-Path $tempLog) { Remove-Item $tempLog -Force }