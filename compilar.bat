@echo off
title Compilar Ejemplos de Librerías
echo ============================================================
echo   Compilando Panel de Control de Ejemplos de Librerías
echo ============================================================
echo.
python -m PyInstaller --onefile --noconsole --name "EjemplosLibrerias" --clean --noconfirm main.py
if %ERRORLEVEL% EQU 0 (
    copy /Y dist\EjemplosLibrerias.exe .\EjemplosLibrerias.exe >nul
    echo.
    echo ============================================================
    echo   [EXITO] Compilacion completada con exito.
    echo   El ejecutable esta listo: EjemplosLibrerias.exe
    echo ============================================================
) else (
    echo.
    echo   [ERROR] Ocurrio un problema al compilar.
)
echo.
pause
