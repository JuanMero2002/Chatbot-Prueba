// Ejemplo de cómo usar el enlace de WhatsApp en el frontend
// Archivo: frontend/js/chatbot-widget.js o similar

// Cuando recibas la respuesta del chatbot:
fetch('/api/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        message: "¿Cómo me contacto?",
        session_id: sessionId
    })
})
.then(response => response.json())
.then(data => {
    // Mostrar el mensaje de respuesta
    displayMessage(data.response, 'bot');
    
    // SI hay un enlace de WhatsApp, mostrar un botón
    if (data.whatsapp_url) {
        // Opción 1: Crear un botón directo
        const whatsappButton = document.createElement('a');
        whatsappButton.href = data.whatsapp_url;
        whatsappButton.className = 'whatsapp-button';
        whatsappButton.textContent = '📱 Abrir WhatsApp';
        whatsappButton.target = '_blank';
        
        // Agregar el botón después del mensaje
        const messageContainer = document.querySelector('.chat-messages');
        messageContainer.appendChild(whatsappButton);
        
        // Opción 2: Mostrar como un botón flotante
        // showFloatingWhatsappButton(data.whatsapp_url);
    }
})
.catch(error => console.error('Error:', error));


// ============================================================
// EJEMPLO DE RESPUESTA DEL SERVIDOR (JSON)
// ============================================================

/*
{
    "response": "📞 **Nuestros Canales de Contacto**\n\n**WhatsApp (Directo):**\n+593 982840675 | +593 962018222 | +593 989831819\n\n🔗 **Abrir WhatsApp Directo:**\nToca el botón de abajo para chatear con nosotros en WhatsApp\n\n**Correo Electrónico:**\ninfo@sparksenergy.io\n\n**Horario de Atención:**\nLunes a Sábado, 08:00 AM – 08:00 PM\n\n**Ubicación:**\nEdificio Manta Business Center, Torre B, Piso 3, Oficina 301\nAv. Malecón (Frente al Mall del Pacífico), Manta, Manabí, Ecuador\n\n¿Prefieres abrir WhatsApp ahora para una consulta rápida?",
    "session_id": "default-session",
    "intent": "contacto",
    "estado": "mostrando_contacto",
    "timestamp": "2026-01-30T14:35:00.000Z",
    "whatsapp_url": "https://wa.me/593982840675?text=Hola%20Sparks%20IoT%26Energy%2C%20me%20gustaría%20recibir%20información%20sobre%20sus%20servicios"
}
*/


// ============================================================
// ESTILOS CSS PARA EL BOTÓN DE WHATSAPP
// ============================================================

/*
.whatsapp-button {
    display: inline-block;
    background-color: #25D366;  /* Color oficial de WhatsApp */
    color: white;
    padding: 12px 24px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: bold;
    margin: 15px 0;
    transition: background-color 0.3s ease;
    border: none;
    cursor: pointer;
    font-size: 16px;
}

.whatsapp-button:hover {
    background-color: #20BA5A;
    text-decoration: none;
    color: white;
}

.whatsapp-button:active {
    transform: scale(0.98);
}

/* Para dispositivos móviles */
@media (max-width: 600px) {
    .whatsapp-button {
        width: 100%;
        text-align: center;
        padding: 15px;
        font-size: 18px;
    }
}
*/


// ============================================================
// FUNCIÓN PARA MOSTRAR BOTÓN FLOTANTE DE WHATSAPP
// ============================================================

function showFloatingWhatsappButton(whatsappUrl) {
    // Crear contenedor flotante
    const floatingButton = document.createElement('div');
    floatingButton.id = 'floating-whatsapp';
    floatingButton.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: #25D366;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 9999;
        animation: pulse 2s infinite;
    `;
    
    // Crear icono (usando emoji)
    const icon = document.createElement('a');
    icon.href = whatsappUrl;
    icon.target = '_blank';
    icon.textContent = '💬';
    icon.style.cssText = `
        font-size: 30px;
        text-decoration: none;
        color: white;
    `;
    
    floatingButton.appendChild(icon);
    document.body.appendChild(floatingButton);
    
    // Agregar animación de pulso en CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
    `;
    document.head.appendChild(style);
}
