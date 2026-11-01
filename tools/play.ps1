# Run by double-clicking เล่นเกม.bat in the repo root: starts a small web server there and opens the game.
# Closing the window stops the server. Saved as UTF-8 with BOM so Windows PowerShell 5.1 reads the Thai text.
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = 'Last Signal'
Set-Location (Split-Path $PSScriptRoot -Parent)
$port = 8000
$url = "http://localhost:$port"
$ip = $null
try { $ip = (Get-NetIPConfiguration).Where({ $_.IPv4DefaultGateway })[0].IPv4Address[0].IPAddress } catch {}

Write-Host ''
Write-Host '  Last Signal'
Write-Host '  ----------------------------------------'
Write-Host "  เล่นบนคอม:     $url"
if ($ip) { Write-Host "  เล่นบนมือถือ:  http://${ip}:$port   (ต่อ Wi-Fi เดียวกับคอม)" }
Write-Host ''

# already running (for example from the Claude app): just open the browser
if (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) {
    Write-Host '  ตัวรันเกมเปิดอยู่แล้ว กำลังเปิดเบราว์เซอร์...'
    Start-Process $url
    Start-Sleep 8
    exit
}

$py = @('python', 'py') | Where-Object { Get-Command $_ -ErrorAction SilentlyContinue } | Select-Object -First 1
if (-not $py) {
    Write-Host '  เปิดเกมไม่ได้ - เครื่องนี้ต้องมี Python'
    Read-Host '  กด Enter เพื่อปิด'
    exit
}
Write-Host '  ปิดหน้าต่างนี้ = ปิดเกม'
Write-Host ''
$server = Start-Process $py -ArgumentList '-m', 'http.server', $port -NoNewWindow -PassThru
Start-Sleep 1
Start-Process $url
$server.WaitForExit()
