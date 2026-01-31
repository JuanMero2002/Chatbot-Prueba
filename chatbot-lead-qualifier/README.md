# Chatbot Sparks IoT&Energy - Lead Qualifier

> Sistema inteligente de calificación de leads para servicios de energía renovable, eficiencia energética e industria 4.0.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Descripción

Chatbot conversacional desarrollado para **Sparks IoT&Energy** (Manta, Ecuador) que ayuda a calificar clientes potenciales interesados en:
- Sistemas de energía solar (On-Grid, Off-Grid, Híbridos)
- Bombeo solar para agricultura
- Iluminación LED solar
- Eficiencia energética y auditorías ISO 50001
- Automatización industrial e IoT

El sistema identifica intenciones, proporciona información detallada y redirige leads calificados a WhatsApp para asesoría personalizada.

---

## ✨ Características Principales

- 🤖 **Conversación Natural**: Detección inteligente de 15+ intenciones diferentes
- 📊 **Gestión de Estados**: Máquina de estados para seguimiento contextual de conversaciones
- 💬 **Integración WhatsApp**: Redirección directa con mensajes pre-formateados
- 📚 **Base de Conocimientos**: JSON estructurado con información de servicios, proyectos y empresa
- 🎯 **Calificación de Leads**: Sistema de scoring basado en interacción
- 🌐 **Widget Web**: Interfaz de chat embebible en sitios web
- 🔒 **Rate Limiting**: Protección contra abuso con límites configurables
- 📝 **Logging Avanzado**: Registro detallado de conversaciones e intenciones

---

## 🏗️ Arquitectura del Proyecto

```
chatbot-lead-qualifier/
├── app/
│   ├── api/                    # Endpoints y lógica de API
│   │   ├── routes.py          # Rutas principales y lógica del chatbot
│   │   └── middleware.py      # Middleware de autenticación/logging
│   ├── chatbot/               # Motor del chatbot
│   │   ├── knowledge_base.json  # Base de datos de conocimientos
│   │   ├── intent_classifier.py # Clasificador de intenciones
│   │   ├── response_generator.py # Generador de respuestas
│   │   └── conversation_manager.py # Gestor de conversaciones
│   ├── integrations/          # Integraciones externas
│   │   ├── whatsapp.py       # Integración WhatsApp Business
│   │   ├── wordpress.py      # Plugin WordPress
│   │   └── email_notifier.py # Notificaciones email
│   ├── models/                # Modelos de datos
│   │   ├── conversation.py   # Modelo de conversación
│   │   ├── lead.py          # Modelo de lead
│   │   └── message.py       # Modelo de mensaje
│   ├── config.py             # Configuración de la aplicación
│   └── main.py              # Factory de la aplicación Flask
├── frontend/                 # Interfaz web del chatbot
│   ├── index.html           # Página de demostración
│   ├── js/
│   │   ├── chatbot-widget.js  # Widget del chat
│   │   └── api-client.js      # Cliente API REST
│   └── css/
│       └── chatbot-styles.css # Estilos del widget
├── tests/                    # Suite de pruebas
├── deployment/              # Configuraciones de despliegue
│   ├── apache/             # Apache + mod_wsgi
│   ├── nginx/              # Nginx + Gunicorn
│   └── systemd/            # Servicios systemd
├── docs/                   # Documentación técnica
├── requirements.txt        # Dependencias Python
├── run.py                 # Script de inicio
└── README.md              # Este archivo
```

---

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes)
- Entorno virtual (recomendado)

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-repositorio>
   cd chatbot-lead-qualifier
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   
   Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

6. **Ejecutar la aplicación**
   ```bash
   python run.py
   ```

7. **Acceder al chatbot**
   
   Abrir en navegador: `http://localhost:5000`

---

## ⚙️ Configuración

Editar el archivo `.env` con tus variables:

```env
# Flask Configuration
DEBUG=True
HOST=0.0.0.0
PORT=5000
SECRET_KEY=tu-clave-secreta-aqui

# CORS Origins (separados por coma)
CORS_ORIGINS=http://localhost:3000,https://tudominio.com

# Database (opcional - actualmente usa sesiones en memoria)
DATABASE_URL=postgresql://user:pass@localhost/chatbot_db

# WhatsApp Business API (para integración futura)
WHATSAPP_API_TOKEN=your-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-id

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_HOUR=100
```

---

## 🎯 Uso del API

### Endpoint Principal: Chat

**POST** `/api/chat`

Request:
```json
{
  "message": "Hola, quiero información sobre energía solar",
  "session_id": "unique-session-id"
}
```

Response:
```json
{
  "response": "Texto de respuesta del chatbot...",
  "session_id": "unique-session-id",
  "intent": "servicio_solar_red",
  "estado": "esperando_confirmacion",
  "whatsapp_url": "https://wa.me/593982840675?text=...",
  "timestamp": "2026-01-31T00:00:00"
}
```

### Intenciones Soportadas

- `saludo` - Mensaje de bienvenida
- `servicio_solar_red` - Sistema solar conectado a red
- `servicio_solar_aislada` - Sistema solar autónomo
- `servicio_bombeo` - Bombeo solar
- `servicio_iluminacion` - Iluminación LED solar
- `servicio_eficiencia` - Eficiencia energética
- `servicio_industria` - Automatización industrial
- `consulta_energias_renovables` - Información general renovables
- `consulta_multiples_servicios` - Múltiples servicios
- `caso_real` - Evaluación de caso específico
- `consulta_procesos` - Proceso de implementación
- `consulta_proyectos` - Proyectos de referencia
- `redes_sociales` - Redes sociales de la empresa
- `contacto` - Información de contacto
- `precio` - Consulta de precios
- `confirmacion_si/no` - Confirmaciones
- `cierre_conversacion` - Finalizar chat

---

## 🧪 Testing

Ejecutar pruebas:
```bash
# Todas las pruebas
pytest

# Con cobertura
pytest --cov=app tests/

# Prueba específica
pytest tests/test_chatbot.py -v
```

---

## 📦 Despliegue en Producción

### Opción 1: Apache + mod_wsgi

```bash
# Instalar Apache y mod_wsgi
sudo apt install apache2 libapache2-mod-wsgi-py3

# Copiar configuración
sudo cp deployment/apache/chatbot.conf /etc/apache2/sites-available/
sudo a2ensite chatbot
sudo systemctl restart apache2
```

### Opción 2: Nginx + Gunicorn

```bash
# Instalar Nginx y Gunicorn
pip install gunicorn
sudo apt install nginx

# Configurar servicio systemd
sudo cp deployment/systemd/chatbot.service /etc/systemd/system/
sudo systemctl enable chatbot
sudo systemctl start chatbot

# Configurar Nginx
sudo cp deployment/nginx/chatbot.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/chatbot.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

---

## 🔌 Integraciones

### WhatsApp Business

Configurar webhook en `WHATSAPP_INTEGRATION.js` para recibir y enviar mensajes.

### WordPress Plugin

Instalar plugin desde `wordpress-plugin/` para integrar el chatbot en sitios WordPress.

---

## 📊 Base de Conocimientos

El chatbot obtiene información de `app/chatbot/knowledge_base.json`:

```json
{
  "empresa": { ... },
  "servicios": [ ... ],
  "proyectos_realizados": [ ... ],
  "contacto": { ... }
}
```

Para actualizar información, editar este archivo y reiniciar la aplicación.

---

## 🛠️ Tecnologías

- **Backend**: Flask 3.0.0
- **CORS**: Flask-CORS 4.0.0
- **Rate Limiting**: Flask-Limiter 3.5.0
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Storage**: Sesiones en memoria (migración a DB pendiente)

---

## 📝 Roadmap

- [ ] Implementar persistencia en base de datos (PostgreSQL)
- [ ] Completar integración WhatsApp Business API
- [ ] Sistema de analytics y métricas
- [ ] Panel de administración
- [ ] Multilengua (ES/EN)
- [ ] IA/ML para clasificación avanzada de intenciones
- [ ] Tests unitarios completos

---

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👥 Equipo

**Sparks IoT&Energy**  
📍 Edificio Manta Business Center, Torre B, Piso 3, Oficina 301  
📍 Manta, Manabí, Ecuador  
📧 info@sparksenergy.io  
📱 WhatsApp: +593 982840675  

---

## 🐛 Reportar Problemas

Si encuentras un bug o tienes una sugerencia, por favor abre un [issue](https://github.com/tu-repo/issues).

---

**Desarrollado con ❤️ para un futuro energético sostenible**
