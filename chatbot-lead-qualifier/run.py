#!/usr/bin/env python3
"""
Script para ejecutar la aplicación en modo desarrollo
"""
from app.main import app
from app.config import Config

if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
