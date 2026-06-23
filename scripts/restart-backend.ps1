# Restart only the backend FastAPI service
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

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

# Stop existing backend process(es)
$procs = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*uvicorn*' }
foreach ($proc in $procs) {
    Write-Host "Stopping backend PID $($proc.ProcessId)" -ForegroundColor Yellow
    Stop-Process -Id $proc.ProcessId -Force
}

# Wait briefly for port release
Start-Sleep -Seconds 2

# Start backend
$projectRoot = Split-Path -Parent $PSScriptRoot
$backendDir = Join-Path $projectRoot "backend"
$venvPython = Join-Path $backendDir "venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: Python venv not found at $venvPython" -ForegroundColor Red
    exit 1
}
Start-Process -FilePath $venvPython -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 16060" -WindowStyle Hidden -WorkingDirectory $backendDir
if (-not (Wait-ForPort 16060 "Backend" 30)) { exit 1 }
Write-Host "Backend restarted on port 16060" -ForegroundColor Green
