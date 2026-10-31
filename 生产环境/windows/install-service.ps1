# ============================================
# 安装为 Windows 服务（开机自启 + 崩溃自动重启）
# 使用 NSSM (Non-Sucking Service Manager)
# 下载 NSSM: https://nssm.cc/download
# 用法: 右键 PowerShell -> 以管理员身份运行 -> ./install-service.ps1
# ============================================

$ErrorActionPreference = "Stop"

$projectDir = Split-Path -Parent $PSScriptRoot | Split-Path -Parent
$venvPython = Join-Path $projectDir ".venv\Scripts\python.exe"
$runScript  = Join-Path $PSScriptRoot "run_prod.py"
$serviceName = "WaterPlantApp"
$nssmPath = "C:\nssm\nssm.exe"   # 请将 nssm.exe 放在此路径

Write-Host "=== 安装水厂主体软件为 Windows 服务 ===" -ForegroundColor Cyan

if (-not (Test-Path $nssmPath)) {
    Write-Host "[错误] 未找到 NSSM，请先下载并解压到 C:\nssm\" -ForegroundColor Red
    Write-Host "下载地址: https://nssm.cc/download"
    exit 1
}

# 安装服务
& $nssmPath install $serviceName $venvPython $runScript
& $nssmPath set $serviceName AppDirectory $projectDir
& $nssmPath set $serviceName DisplayName "水厂主体软件"
& $nssmPath set $serviceName Description "水厂主体软件 - Flask Web + 控制台常驻任务"
& $nssmPath set $serviceName Start SERVICE_AUTO_START
& $nssmPath set $serviceName AppStdout "$projectDir\logs\app-out.log"
& $nssmPath set $serviceName AppStderr "$projectDir\logs\app-err.log"

# 创建日志目录
New-Item -ItemType Directory -Path "$projectDir\logs" -Force | Out-Null

# 启动服务
Start-Service $serviceName
Write-Host ""
Write-Host "[完成] 服务已安装并启动！" -ForegroundColor Green
Write-Host "服务名称: $serviceName"
Write-Host "Web 地址: http://localhost/"
Write-Host ""
Write-Host "常用命令:"
Write-Host "  启动: net start $serviceName"
Write-Host "  停止: net stop $serviceName"
Write-Host "  卸载: $nssmPath remove $serviceName"
