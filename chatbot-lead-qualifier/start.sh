#!/bin/bash
# Script de inicio rápido para Linux/Mac
# Chatbot Sparks IoT&Energy

set -e

echo "============================================"
echo "Chatbot Sparks IoT&Energy - Inicio Rápido"
echo "============================================"
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "[!] No se encontró entorno virtual"
    echo "[+] Creando entorno virtual..."
    python3 -m venv venv
    echo "[OK] Entorno virtual creado"
    echo ""
fi

# Activar entorno virtual
echo "[+] Activando entorno virtual..."
source venv/bin/activate

# Verificar si hay dependencias instaladas
if ! python -c "import flask" 2>/dev/null; then
    echo "[!] Dependencias no instaladas"
    echo "[+] Instalando dependencias..."
    pip install -r requirements.txt
    echo "[OK] Dependencias instaladas"
    echo ""
fi

# Verificar archivo .env
if [ ! -f ".env" ]; then
    echo "[!] No se encontró archivo .env"
    if [ -f ".env.example" ]; then
        echo "[+] Copiando .env.example a .env"
        cp .env.example .env
        echo "[!] IMPORTANTE: Edita el archivo .env con tus configuraciones"
        echo ""
    else
        echo "[ERROR] No se encontró .env.example"
        exit 1
    fi
fi

# Iniciar servidor
echo "[+] Iniciando servidor..."
echo ""
echo "Presiona Ctrl+C para detener el servidor"
echo ""
python run.py
