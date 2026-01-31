#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chatbot Sparks IoT&Energy - Lead Qualifier
Script de inicialización para entorno de desarrollo

Este script inicia el servidor Flask en modo desarrollo.
Para producción, usar Gunicorn o mod_wsgi.

Usage:
    python run.py
    
Environment Variables:
    DEBUG: Modo debug (True/False)
    HOST: Host del servidor (default: 0.0.0.0)
    PORT: Puerto del servidor (default: 5000)
"""

import sys
import os
from pathlib import Path

# Asegurar que el directorio raíz está en el path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

try:
    from app.main import app
    from app.config import Config
except ImportError as e:
    print(f"Error importando módulos: {e}")
    print("Asegúrate de haber instalado las dependencias:")
    print("  pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Función principal para iniciar el servidor"""
    try:
        print("=" * 60)
        print("Chatbot Sparks IoT&Energy - Iniciando...")
        print("=" * 60)
        print(f"Modo Debug: {Config.DEBUG}")
        print(f"Host: {Config.HOST}")
        print(f"Puerto: {Config.PORT}")
        print("=" * 60)
        
        if Config.DEBUG:
            print("ATENCION: Modo DEBUG activado - Solo para desarrollo")
            print("Para producción, usar Gunicorn o mod_wsgi")
            print("=" * 60)
        
        # Iniciar servidor Flask
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG,
            use_reloader=Config.DEBUG,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n\nServidor detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\nError iniciando el servidor: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
