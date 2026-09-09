# run.ps1 - ตัวช่วยรันสคริปต์ Week9 บน Windows
# วิธีใช้:  .\run.ps1 student2_pit_strategy_engineer.py
#
# ทำไมต้องมีไฟล์นี้: เทอร์มินอล Windows ปกติเป็น cp1252 พอโค้ด print emoji
# จะพังด้วย UnicodeEncodeError ไฟล์นี้ตั้ง encoding เป็น utf-8 ให้อัตโนมัติ
#
# หมายเหตุ: ไฟล์นี้ต้องเซฟเป็น UTF-8 with BOM เท่านั้น
# ไม่งั้น PowerShell 5.1 จะอ่านคอมเมนต์ภาษาไทยเพี้ยนแล้ว parse error

param(
    [Parameter(Mandatory = $true)]
    [string]$Script
)

# ตั้ง encoding ก่อนพิมพ์อะไรทั้งสิ้น
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

if (-not (Test-Path $Script)) {
    Write-Host "File not found: $Script" -ForegroundColor Red
    Write-Host "Available scripts in this folder:" -ForegroundColor Yellow
    Get-ChildItem -Filter *.py | ForEach-Object { "  " + $_.Name }
    exit 1
}

Write-Host "PYTHONIOENCODING=utf-8  |  running $Script" -ForegroundColor Green
python $Script
