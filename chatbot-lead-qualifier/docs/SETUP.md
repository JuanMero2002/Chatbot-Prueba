# Guía de Instalación

## Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- MySQL o PostgreSQL
- Git

## Pasos de instalación

### 1. Clonar o descargar el proyecto

```bash
git clone <url-del-repo>
cd chatbot-lead-qualifier
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

### 6. Configurar base de datos

```bash
python -c "from app.database.connection import init_db; init_db()"
```

### 7. Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## Despliegue en producción

Ver sección de despliegue en la documentación.

