@echo off
chcp 65001 >nul
echo ============================================
echo   肠道菌群检测报告生成器 v2.0 - 安装与启动
echo ============================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装Python 3.9+
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/3] 正在检查Python环境...
python --version

echo.
echo [2/3] 正在安装依赖包...
pip install -r requirements.txt -q

echo.
echo [3/3] 正在启动程序...
echo.
python main.py

pause
