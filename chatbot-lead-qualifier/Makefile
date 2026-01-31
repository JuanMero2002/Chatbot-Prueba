# Makefile para Chatbot Sparks IoT&Energy
# Facilita tareas comunes de desarrollo

.PHONY: help install run test clean lint format

# Variables
PYTHON := python
PIP := pip
PYTEST := pytest
BLACK := black
FLAKE8 := flake8

help:  ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Instalar dependencias
	$(PIP) install -r requirements.txt

install-dev:  ## Instalar dependencias de desarrollo
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 mypy

run:  ## Ejecutar servidor de desarrollo
	$(PYTHON) run.py

test:  ## Ejecutar todos los tests
	$(PYTEST) tests/ -v

test-cov:  ## Ejecutar tests con cobertura
	$(PYTEST) --cov=app --cov-report=html --cov-report=term tests/

test-unit:  ## Ejecutar solo tests unitarios
	$(PYTEST) tests/ -v -m unit

test-integration:  ## Ejecutar solo tests de integración
	$(PYTEST) tests/ -v -m integration

lint:  ## Verificar estilo de código
	$(FLAKE8) app/ --max-line-length=100

format:  ## Formatear código con black
	$(BLACK) app/ tests/ --line-length=100

clean:  ## Limpiar archivos temporales
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

setup:  ## Configurar entorno completo
	$(PYTHON) -m venv venv
	@echo "Entorno virtual creado. Actívalo con:"
	@echo "  Windows: venv\\Scripts\\activate"
	@echo "  Linux/Mac: source venv/bin/activate"
	@echo "Luego ejecuta: make install"

db-init:  ## Inicializar base de datos
	$(PYTHON) -c "from app.database.connection import init_db; init_db()"

db-migrate:  ## Ejecutar migraciones
	@echo "Migraciones no implementadas aún"

prod-check:  ## Verificar configuración para producción
	@echo "Verificando configuración de producción..."
	@grep -q "DEBUG=False" .env && echo "✓ DEBUG está en False" || echo "✗ WARNING: DEBUG está en True"
	@grep -q "SECRET_KEY=" .env && echo "✓ SECRET_KEY configurado" || echo "✗ ERROR: SECRET_KEY no configurado"

deploy-apache:  ## Desplegar con Apache
	sudo cp deployment/apache/chatbot.conf /etc/apache2/sites-available/
	sudo a2ensite chatbot
	sudo systemctl restart apache2

deploy-nginx:  ## Desplegar con Nginx
	sudo cp deployment/nginx/chatbot.conf /etc/nginx/sites-available/
	sudo ln -s /etc/nginx/sites-available/chatbot.conf /etc/nginx/sites-enabled/
	sudo systemctl restart nginx

logs:  ## Ver logs en tiempo real
	tail -f logs/chatbot.log

.DEFAULT_GOAL := help
