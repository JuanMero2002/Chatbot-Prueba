@echo off
REM Script de inicio rápido para Windows
REM Chatbot Sparks IoT&Energy

echo ============================================
echo Chatbot Sparks IoT^&Energy - Inicio Rapido
echo ============================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo [!] No se encontro entorno virtual
    echo [+] Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual creado
    echo.
)

REM Activar entorno virtual
echo [+] Activando entorno virtual...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] No se pudo activar el entorno virtual
    pause
    exit /b 1
)

REM Verificar si hay dependencias instaladas
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [!] Dependencias no instaladas
    echo [+] Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Error instalando dependencias
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas
    echo.
)

REM Verificar archivo .env
if not exist ".env" (
    echo [!] No se encontro archivo .env
    if exist ".env.example" (
        echo [+] Copiando .env.example a .env
        copy .env.example .env
        echo [!] IMPORTANTE: Edita el archivo .env con tus configuraciones
        echo.
    ) else (
        echo [ERROR] No se encontro .env.example
        pause
        exit /b 1
    )
)

REM Iniciar servidor
echo [+] Iniciando servidor...
echo.
echo Presiona Ctrl+C para detener el servidor
echo.
python run.py

pause
