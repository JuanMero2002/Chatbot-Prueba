# Plugin de WordPress - Sparks IoT & Energy Chatbot

## Descripción

Plugin profesional de chatbot para WordPress que integra el sistema de atención al cliente de Sparks IoT & Energy. Genera leads cualificados y proporciona información automatizada sobre servicios de energías renovables.

## Características

- **Widget Flotante**: Botón flotante personalizable en cualquier página
- **Interfaz Moderna**: Diseño responsive y profesional
- **Integración API**: Conecta con el backend Flask del chatbot
- **Persistencia de Sesiones**: Mantiene conversaciones entre visitas
- **WhatsApp Integration**: Botones directos para contacto por WhatsApp
- **Panel de Administración**: Configuración completa desde WordPress
- **Shortcode**: Inserta el chatbot en cualquier página o entrada
- **Multiposición**: Configura la posición del widget (derecha/izquierda)

## Instalación

### Método 1: Instalación Manual

1. Descarga el directorio `wordpress-plugin`
2. Renombra la carpeta a `sparks-chatbot`
3. Sube la carpeta a `/wp-content/plugins/` de tu WordPress
4. Activa el plugin desde el panel de Plugins
5. Configura la URL de la API en Ajustes > Chatbot Sparks

### Método 2: Instalación ZIP

1. Comprime el directorio `wordpress-plugin` en `sparks-chatbot.zip`
2. Ve a Plugins > Añadir nuevo > Subir plugin
3. Selecciona el archivo ZIP y haz clic en Instalar
4. Activa el plugin
5. Configura desde Ajustes > Chatbot Sparks

## Configuración

### Requisitos Previos

Asegúrate de que el servidor Flask del chatbot esté corriendo:

```bash
cd chatbot-lead-qualifier
python run.py
```

El servidor debe estar accesible en `http://127.0.0.1:5000` o la URL que configures.

### Configuración del Plugin

1. Ve a **Ajustes > Chatbot Sparks**
2. Configura los siguientes parámetros:

| Parámetro | Descripción | Valor por Defecto |
|-----------|-------------|-------------------|
| Habilitar Chatbot | Activa/desactiva el widget | Activado |
| URL de la API | Endpoint del servidor Flask | http://127.0.0.1:5000/api |
| Título | Nombre mostrado en el header | Sparks IoT & Energy |
| Subtítulo | Descripción corta | Chatbot de atención al cliente |
| Mensaje de Bienvenida | Primer mensaje automático | ¡Hola! ¿En qué puedo ayudarte hoy? |
| Posición | Ubicación del botón flotante | Abajo Derecha |
| Color Principal | Color del tema del chatbot | #2563eb |

3. Haz clic en **Guardar Configuración**

## Uso

### Widget Flotante

El chatbot aparece automáticamente como un botón flotante en todas las páginas de tu sitio web cuando está activado.

### Shortcode

Puedes insertar el chatbot en cualquier página o entrada usando el shortcode:

```php
[sparks_chatbot]
```

**Con parámetros opcionales:**

```php
[sparks_chatbot inline="true" height="600px"]
```

### Ejemplos de Uso

**En una página de contacto:**
```php
<h2>Chatea con nosotros</h2>
[sparks_chatbot inline="true"]
```

**En un widget de texto:**
```php
[sparks_chatbot]
```

**En plantillas PHP:**
```php
<?php echo do_shortcode('[sparks_chatbot]'); ?>
```

## Estructura de Archivos

```
wordpress-plugin/
├── chatbot-plugin.php          # Archivo principal del plugin
├── README.md                    # Documentación
├── assets/
│   ├── css/
│   │   └── chatbot.css         # Estilos del chatbot
│   └── js/
│       └── chatbot.js          # JavaScript del chatbot
├── templates/
│   ├── chatbot-widget.php      # Template del widget flotante
│   ├── chatbot-inline.php      # Template inline (shortcode)
│   └── admin-settings.php      # Página de configuración admin
└── includes/
    └── api-integration.php     # Funciones de integración API
```

## API del Chatbot

El plugin se comunica con el backend Flask mediante los siguientes endpoints:

### POST /api/chat
Envía un mensaje al chatbot y recibe una respuesta.

**Request:**
```json
{
    "message": "Hola",
    "session_id": "wp_session_123456"
}
```

**Response:**
```json
{
    "response": "¡Hola! Bienvenido...",
    "session_id": "wp_session_123456",
    "intent": "saludo",
    "estado": "presentacion",
    "whatsapp_url": "https://wa.me/593985937244?text=..."
}
```

### GET /api/health
Verifica el estado del servidor.

**Response:**
```json
{
    "status": "healthy",
    "service": "Sparks IoT & Energy",
    "timestamp": "2026-01-30T10:00:00"
}
```

## Personalización

### Cambiar Colores

Edita el archivo `assets/css/chatbot.css`:

```css
:root {
    --sparks-chatbot-color: #2563eb;
    --sparks-chatbot-color-hover: #1d4ed8;
}
```

O usa el selector de color en la página de configuración.

### Modificar Mensajes

Los mensajes están centralizados en el backend Flask. Para modificarlos, edita:

```
chatbot-lead-qualifier/app/api/routes.py
```

### Agregar Funcionalidades

Extiende la clase `Sparks_Chatbot_Plugin` en `chatbot-plugin.php`:

```php
add_filter('sparks_chatbot_response', function($response) {
    // Tu código aquí
    return $response;
});
```

## Solución de Problemas

### El chatbot no aparece

1. Verifica que el plugin esté activado
2. Confirma que "Habilitar Chatbot" esté marcado en la configuración
3. Limpia el caché de WordPress
4. Revisa la consola del navegador para errores JavaScript

### Error "No disponible" en la API

1. Verifica que el servidor Flask esté corriendo:
   ```bash
   curl http://127.0.0.1:5000/api/health
   ```
2. Confirma la URL de la API en la configuración
3. Revisa los logs del servidor Flask
4. Si usas hosting externo, asegúrate de que el puerto esté abierto

### El chatbot no responde

1. Abre las herramientas de desarrollador (F12)
2. Ve a la pestaña "Network" y envía un mensaje
3. Revisa si hay errores en las peticiones AJAX
4. Verifica los logs de PHP en WordPress

### Problemas de CORS

Si el servidor Flask está en un dominio diferente, agrega CORS:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://tu-sitio.com"}})
```

## Seguridad

- El plugin usa nonces de WordPress para proteger peticiones AJAX
- Sanitiza todas las entradas del usuario
- Valida y escapa datos antes de mostrarlos
- No almacena información sensible en el navegador

### Recomendaciones de Producción

1. **SSL/HTTPS**: Usa siempre HTTPS en producción
2. **API Externa**: Aloja el servidor Flask en un servidor dedicado
3. **Rate Limiting**: Implementa límites de peticiones en el servidor
4. **Logging**: Monitorea las peticiones y errores
5. **Backup**: Mantén respaldos de la configuración

## Compatibilidad

- **WordPress**: 5.0 o superior
- **PHP**: 7.4 o superior
- **Navegadores**: Chrome, Firefox, Safari, Edge (últimas 2 versiones)
- **Responsive**: Compatible con dispositivos móviles

## Desinstalación

El plugin limpia automáticamente al desinstalarse:

1. Desactiva el plugin
2. Elimina el plugin desde WordPress
3. Las opciones de configuración se eliminan automáticamente

## Soporte

Para soporte técnico, contacta:

- **Email**: info@sparksenergy.io
- **Teléfonos**: +593 982840675 / +593 984141479
- **WhatsApp**: +593 985937244
- **Web**: https://sparksenergy.io

## Licencia

GPL v2 or later

## Changelog

### Versión 1.0.0 (2026-01-30)
- Lanzamiento inicial
- Widget flotante con diseño moderno
- Panel de administración completo
- Integración con API Flask
- Shortcode para inserción manual
- Soporte para WhatsApp
- Sistema de sesiones persistentes
- Responsive design

## Créditos

Desarrollado por Sparks IoT & Energy
