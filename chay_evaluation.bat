@echo off
chcp 65001 >nul
title CO-SPY Enhanced — Chạy Đánh Giá Mô Hình
color 0A

echo.
echo  =========================================================
echo    CO-SPY ENHANCED — Notebook Đánh Giá Chỉ Số Mô Hình
echo  =========================================================
echo.
echo  File chạy: evaluation_metrics.ipynb
echo  Mở trình duyệt tại: http://localhost:8888
echo.

cd /d "%~dp0"

REM Kiểm tra jupyter
where jupyter >nul 2>&1
if errorlevel 1 (
    echo [!] Jupyter chưa cài. Đang cài...
    pip install jupyter notebook ipywidgets scikit-learn pandas matplotlib seaborn -q
    echo [OK] Đã cài xong.
)

echo [*] Khởi động Jupyter Notebook...
echo [*] Notebook sẽ tự mở trong trình duyệt.
echo.
echo     ► Vào Cell Menu → Run All Cells để chạy toàn bộ
echo     ► Hoặc Shift+Enter từng cell để chạy từng bước
echo.
start "" jupyter notebook evaluation_metrics.ipynb --no-browser
timeout /t 2 /nobreak >nul
start "" http://localhost:8888/notebooks/evaluation_metrics.ipynb

echo.
echo [*] Nhấn Ctrl+C để dừng Jupyter server
pause >nul
