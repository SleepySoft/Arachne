#requires -Version 5.1
<#
.SYNOPSIS
    一键停止 Arachne 全系统（Neo4j + 后端 + 前端）
#>
$ErrorActionPreference = "SilentlyContinue"

function Stop-ByPort($port, $label) {
    $conn = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Where-Object { $_.OwningProcess -ne 0 } | Select-Object -First 1
    if ($conn) {
        $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
        if ($proc) {
            Stop-Process -Id $proc.Id -Force
            Write-Host "  $label stopped (PID $($proc.Id))" -ForegroundColor Green
            return
        }
    }
    Write-Host "  $label not running on port $port" -ForegroundColor DarkGray
}

Write-Host "[1/3] Stopping Frontend..." -ForegroundColor Cyan
Stop-ByPort 3000 "Frontend"

Write-Host "[2/3] Stopping Backend..." -ForegroundColor Cyan
Stop-ByPort 16060 "Backend"

Write-Host "[3/3] Stopping Neo4j..." -ForegroundColor Cyan
# Neo4j runs on 7687 (java process) and 7474 (HTTP)
Stop-ByPort 7687 "Neo4j"
# Double-check port 7474
$conn = Get-NetTCPConnection -LocalPort 7474 -ErrorAction SilentlyContinue | Where-Object { $_.OwningProcess -ne 0 } | Select-Object -First 1
if ($conn) {
    $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
    if ($proc -and $proc.ProcessName -eq "java") {
        Stop-Process -Id $proc.Id -Force
        Write-Host "  Neo4j HTTP stopped (PID $($proc.Id))" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "All services stopped." -ForegroundColor Green
