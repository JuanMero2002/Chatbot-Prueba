# 📱 Integración de Enlaces Directos a WhatsApp

## ¿Qué se implementó?

Cuando el usuario pregunta por **contacto**, ahora el chatbot proporciona:

1. ✅ **Información de contacto tradicional** (email, teléfono, horario)
2. ✅ **Enlace directo a WhatsApp** con un botón verde clicable
3. ✅ **Mensaje pre-escrito** que se abre automáticamente en WhatsApp

---

## 📋 Ejemplo de Conversación

### Usuario pregunta:
```
"¿Cómo me contacto con ustedes?"
o
"¿Cómo puedo hablar con alguien de Sparks?"
o
"Necesito información de contacto"
```

### Respuesta del Bot:
```
📞 **Nuestros Canales de Contacto**

**WhatsApp (Directo):**
+593 982840675 | +593 962018222 | +593 989831819

🔗 **Abrir WhatsApp Directo:**
Toca el botón de abajo para chatear con nosotros en WhatsApp

**Correo Electrónico:**
info@sparksenergy.io

**Horario de Atención:**
Lunes a Sábado, 08:00 AM – 08:00 PM

**Ubicación:**
Edificio Manta Business Center, Torre B, Piso 3, Oficina 301
Av. Malecón (Frente al Mall del Pacífico), Manta, Manabí, Ecuador

¿Prefieres abrir WhatsApp ahora para una consulta rápida?
```

### Botón de WhatsApp:
```
┌─────────────────────────────┐
│  💬 Abrir WhatsApp          │  ← Verde, clicable
└─────────────────────────────┘
```

---

## 🔧 Cómo Funciona Técnicamente

### Backend (app/api/routes.py)

```python
elif intencion == 'contacto':
    contacto = obtener_contacto_empresa()
    whatsapp_numeros = contacto.get('whatsapp', [])
    numero_whatsapp_principal = whatsapp_numeros[0].replace('+', '').replace(' ', '')
    
    # Crear URL de WhatsApp con mensaje pre-escrito
    mensaje_whatsapp = "Hola Sparks IoT&Energy, me gustaría recibir información sobre sus servicios"
    whatsapp_url = f"https://wa.me/{numero_whatsapp_principal}?text={mensaje_whatsapp.replace(' ', '%20')}"
    
    response_text = f"""📞 **Nuestros Canales de Contacto**
    ...
    """
    
    # La URL se incluye en la respuesta JSON
    if numero_whatsapp_principal:
        whatsapp_url = f"https://wa.me/{numero_whatsapp_principal}?text=..."
```

### Respuesta JSON del Servidor

```json
{
    "response": "📞 **Nuestros Canales de Contacto**\n\n...",
    "session_id": "default-session",
    "intent": "contacto",
    "estado": "mostrando_contacto",
    "timestamp": "2026-01-30T14:35:00.000Z",
    "whatsapp_url": "https://wa.me/593982840675?text=Hola%20Sparks%20IoT%26Energy%2C%20me%20gustaría%20recibir%20información%20sobre%20sus%20servicios"
}
```

### Frontend (frontend/js/chatbot-widget.js)

```javascript
try {
    const response = await chatbotAPI.sendMessage(message);
    hideTyping();
    
    // Agregar respuesta del bot
    addMessage(response.response);
    
    // SI hay URL de WhatsApp, agregar botón
    if (response.whatsapp_url) {
        addWhatsAppButton(response.whatsapp_url);  // ← Nueva función
    }
    
} catch (error) {
    // manejo de error
}
```

### Función que Agrega el Botón

```javascript
function addWhatsAppButton(url) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.innerHTML = '<i class="fas fa-robot"></i>';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const buttonLink = document.createElement('a');
    buttonLink.href = url;
    buttonLink.target = '_blank';
    buttonLink.className = 'whatsapp-button';
    buttonLink.innerHTML = '<i class="fab fa-whatsapp"></i> Abrir WhatsApp';
    
    contentDiv.appendChild(buttonLink);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatbotMessages.appendChild(messageDiv);
    scrollToBottom();
}
```

---

## 🎨 Estilos CSS del Botón

```css
.whatsapp-button {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #25D366;  /* Color oficial de WhatsApp */
    color: white;
    padding: 12px 24px;
    border-radius: 25px;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(37, 211, 102, 0.3);
    margin-top: 8px;
}

.whatsapp-button:hover {
    background: #20BA5A;  /* Verde más oscuro al pasar el mouse */
    transform: translateY(-2px);  /* Levanta un poco el botón */
    box-shadow: 0 6px 12px rgba(37, 211, 102, 0.4);
}

.whatsapp-button i {
    font-size: 1.25rem;
}
```

---

## 📱 Qué Ocurre Cuando el Usuario Hace Clic

1. El usuario ve el botón verde de WhatsApp
2. Hace clic en el botón
3. Se abre WhatsApp (en navegador o app del celular)
4. Un nuevo chat se crea automáticamente con el número +593 982840675
5. El mensaje pre-escrito aparece: "Hola Sparks IoT&Energy, me gustaría recibir información sobre sus servicios"
6. El usuario solo necesita presionar enviar o personalizarlo

---

## 🔗 Ejemplos de URLs de WhatsApp

### Estructura básica:
```
https://wa.me/NUMERO_SIN_SIMBOLOS?text=MENSAJE_CODIFICADO
```

### Ejemplos:
```
# Sin mensaje personalizado
https://wa.me/593982840675

# Con mensaje (espacios reemplazados por %20)
https://wa.me/593982840675?text=Hola%20Sparks%20IoT%26Energy

# Con mensaje más largo
https://wa.me/593982840675?text=Hola%20Sparks%20IoT%26Energy%2C%20me%20gustaría%20recibir%20información%20sobre%20sistemas%20solares
```

---

## ✅ Características Implementadas

| Característica | Estado | Detalles |
|---|---|---|
| Detección de "contacto" | ✅ | Activa en 8+ intenciones |
| Botón verde de WhatsApp | ✅ | Con icono y estilos |
| Mensaje pre-escrito | ✅ | Personalizable en código |
| Abre en nueva pestaña | ✅ | No interrumpe el chat |
| Número verificado | ✅ | Del knowledge_base |
| Responsive (móvil) | ✅ | Funciona en cualquier dispositivo |
| Efecto hover | ✅ | Se levanta y oscurece el botón |
| Animación | ✅ | Transición suave |

---

## 🚀 Cómo Probar

### Paso 1: Asegúrate de que el servidor está corriendo
```bash
python run.py
```

### Paso 2: Abre el chatbot
```
http://localhost:5000
```

### Paso 3: Pregunta sobre contacto
```
Escribe: "¿Cómo me contacto?"
o
"Necesito los números de WhatsApp"
o
"Dame información de contacto"
```

### Paso 4: Verifica el botón
- Deberías ver un botón verde con el icono de WhatsApp
- Haz clic en él
- Se abrirá WhatsApp con el mensaje pre-escrito

---

## 🔧 Personalización

### Cambiar el mensaje pre-escrito

En `app/api/routes.py`, línea ~356:

```python
mensaje_whatsapp = "Hola Sparks IoT&Energy, me gustaría recibir información sobre sus servicios"
```

Cámbialo por:

```python
mensaje_whatsapp = "Hola, quiero conocer más sobre vuestros servicios de energía solar"
```

### Cambiar el número de WhatsApp por defecto

El sistema usa el primer número del `knowledge_base.json`, pero puedes especificar otro:

```python
numero_whatsapp_principal = "593962018222"  # Cambiar este número
```

---

## 📊 Respuesta JSON Completa

```json
{
    "response": "📞 **Nuestros Canales de Contacto**\n\n**WhatsApp (Directo):**\n+593 982840675 | +593 962018222 | +593 989831819\n\n🔗 **Abrir WhatsApp Directo:**\nToca el botón de abajo para chatear con nosotros en WhatsApp\n\n**Correo Electrónico:**\ninfo@sparksenergy.io\n\n**Horario de Atención:**\nLunes a Sábado, 08:00 AM – 08:00 PM\n\n**Ubicación:**\nEdificio Manta Business Center, Torre B, Piso 3, Oficina 301\nAv. Malecón (Frente al Mall del Pacífico), Manta, Manabí, Ecuador\n\n¿Prefieres abrir WhatsApp ahora para una consulta rápida?",
    "session_id": "default-session",
    "intent": "contacto",
    "estado": "mostrando_contacto",
    "timestamp": "2026-01-30T14:35:45.123Z",
    "whatsapp_url": "https://wa.me/593982840675?text=Hola%20Sparks%20IoT%26Energy%2C%20me%20gustaría%20recibir%20información%20sobre%20sus%20servicios"
}
```

---

## 🎁 Bonus: Otras Intenciones que También Usan WhatsApp

Actualmente, estas intenciones también pueden devolver `whatsapp_url`:

1. **Consulta de Servicios** - "¿Qué servicios ofrecen?"
2. **Información sobre Proyectos** - "¿Qué casos de éxito tienen?"
3. **Consulta sobre Precios** - "¿Cuánto cuesta?"
4. **Confirmación de interés** - "Sí, me interesa"

---

## 📞 Resumen

✅ El chatbot ahora proporciona un **enlace directo a WhatsApp**  
✅ El botón es **verde, brillante y fácil de ver**  
✅ El usuario ve un **mensaje pre-escrito**  
✅ Se abre **sin interrumpir la conversación**  
✅ Funciona en **móvil, tablet y escritorio**  
✅ **Fácil de personalizar** editando el código  

---

**¡Tu chatbot ahora está más conectado con WhatsApp!** 📱✨
