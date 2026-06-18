#requires -Version 5.1
<#
.SYNOPSIS
    一键启动 Arachne 全系统（Neo4j + 后端 + 前端）
#>
$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition

function Test-Port($port) {
    $conn = Test-NetConnection -ComputerName localhost -Port $port -WarningAction SilentlyContinue
    return $conn.TcpTestSucceeded
}

function Wait-ForPort($port, $label, $timeoutSec = 60) {
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    while ($sw.Elapsed.TotalSeconds -lt $timeoutSec) {
        if (Test-Port $port) {
            Write-Host "  $label ready on port $port" -ForegroundColor Green
            return $true
        }
        Start-Sleep -Milliseconds 500
    }
    Write-Host "  $label failed to start within ${timeoutSec}s" -ForegroundColor Red
    return $false
}

# ── Neo4j ──────────────────────────────────────────────
Write-Host "[1/3] Starting Neo4j..." -ForegroundColor Cyan
if (Test-Port 7687) {
    Write-Host "  Neo4j already running on port 7687" -ForegroundColor Yellow
} else {
    $neo4jHome = Join-Path $projectRoot "neo4j-community-5.26.0"
    if (-not (Test-Path $neo4jHome)) {
        Write-Host "  ERROR: Neo4j not found at $neo4jHome" -ForegroundColor Red
        exit 1
    }
    # Start Neo4j in background using Start-Process so the window is hidden
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c `"$neo4jHome\bin\neo4j.bat`" console" -WindowStyle Hidden -WorkingDirectory $neo4jHome
    if (-not (Wait-ForPort 7687 "Neo4j" 30)) { exit 1 }
}

# ── Backend ────────────────────────────────────────────
Write-Host "[2/3] Starting Backend (FastAPI)..." -ForegroundColor Cyan
if (Test-Port 16060) {
    Write-Host "  Backend already running on port 16060" -ForegroundColor Yellow
} else {
    $backendDir = Join-Path $projectRoot "backend"
    $venvPython = Join-Path $backendDir "venv\Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-Host "  ERROR: Python venv not found at $venvPython" -ForegroundColor Red
        exit 1
    }
    Start-Process -FilePath $venvPython -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 16060" -WindowStyle Hidden -WorkingDirectory $backendDir
    if (-not (Wait-ForPort 16060 "Backend" 30)) { exit 1 }
    # Seed data if graph is empty
    try {
        $resp = Invoke-RestMethod -Uri "http://localhost:16060/api/v1/query/stats" -TimeoutSec 5
        if ($resp.total_nodes -eq 0) {
            Write-Host "  Seeding data..." -ForegroundColor DarkGray
            $payload = Get-Content (Join-Path $projectRoot "data\seed_industry_graph.json") -Raw -Encoding UTF8 | ConvertFrom-Json -Depth 10
            $body = $payload | ConvertTo-Json -Depth 10 -Compress
            Invoke-RestMethod -Uri "http://localhost:16060/api/v1/batches" -Method POST -ContentType "application/json" -Body $body -TimeoutSec 30 | Out-Null
            Write-Host "  Seed data loaded" -ForegroundColor Green
        }
    } catch {
        Write-Host "  Warning: could not seed data: $_" -ForegroundColor Yellow
    }
}

# ── Frontend ───────────────────────────────────────────
Write-Host "[3/3] Starting Frontend (Vite)..." -ForegroundColor Cyan
if (Test-Port 3000) {
    Write-Host "  Frontend already running on port 3000" -ForegroundColor Yellow
} else {
    $frontendDir = Join-Path $projectRoot "frontend"
    Start-Process -FilePath "cmd.exe" -ArgumentList "/c npx vite --host" -WindowStyle Hidden -WorkingDirectory $frontendDir
    if (-not (Wait-ForPort 3000 "Frontend" 30)) { exit 1 }
}

# ── Summary ────────────────────────────────────────────
Write-Host ""
Write-Host "All services are running!" -ForegroundColor Green
Write-Host "  Neo4j Browser:  http://localhost:7474"
Write-Host "  Backend API:    http://localhost:16060/docs"
Write-Host "  Frontend App:   http://localhost:3000"
Write-Host ""
Write-Host "To stop everything, run: .\stop-all.ps1" -ForegroundColor DarkGray
