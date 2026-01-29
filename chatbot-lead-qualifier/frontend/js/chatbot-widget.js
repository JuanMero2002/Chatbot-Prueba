// Chatbot Widget JavaScript

// Inicializar API Client
const chatbotAPI = new ChatbotAPI();

// Elementos del DOM
const chatbotWidget = document.getElementById('chatbot-widget');
const chatbotToggle = document.getElementById('chatbot-toggle');
const chatbotClose = document.getElementById('chatbot-close');
const chatbotMessages = document.getElementById('chatbot-messages');
const chatbotInputField = document.getElementById('chatbot-input-field');
const chatbotSend = document.getElementById('chatbot-send');
const chatbotTyping = document.getElementById('chatbot-typing');
const chatbotBadge = document.getElementById('chatbot-badge');

// Estado
let isOpen = false;
let messageCount = 0;

// Toggle chatbot
function toggleChatbot() {
    isOpen = !isOpen;
    if (isOpen) {
        chatbotWidget.classList.remove('closed');
        chatbotInputField.focus();
        messageCount = 0;
        updateBadge();
    } else {
        chatbotWidget.classList.add('closed');
    }
}

// Actualizar badge
function updateBadge() {
    if (messageCount > 0) {
        chatbotBadge.textContent = messageCount;
        chatbotBadge.style.display = 'flex';
    } else {
        chatbotBadge.style.display = 'none';
    }
}

// Agregar mensaje al chat
function addMessage(text, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = isUser ? 'message user-message' : 'message bot-message';
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';
    avatarDiv.innerHTML = isUser ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textP = document.createElement('p');
    textP.textContent = text;
    
    const timeSpan = document.createElement('span');
    timeSpan.className = 'message-time';
    timeSpan.textContent = getCurrentTime();
    
    contentDiv.appendChild(textP);
    contentDiv.appendChild(timeSpan);
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatbotMessages.appendChild(messageDiv);
    scrollToBottom();
    
    // Incrementar contador si no está abierto
    if (!isUser && !isOpen) {
        messageCount++;
        updateBadge();
    }
}

// Obtener hora actual
function getCurrentTime() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

// Scroll al final
function scrollToBottom() {
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

// Mostrar indicador de escritura
function showTyping() {
    chatbotTyping.style.display = 'block';
    scrollToBottom();
}

// Ocultar indicador de escritura
function hideTyping() {
    chatbotTyping.style.display = 'none';
}

// Enviar mensaje
async function sendMessage() {
    const message = chatbotInputField.value.trim();
    
    if (!message) return;
    
    // Agregar mensaje del usuario
    addMessage(message, true);
    chatbotInputField.value = '';
    
    // Mostrar typing indicator
    showTyping();
    
    try {
        // Enviar a la API
        const response = await chatbotAPI.sendMessage(message);
        
        // Simular delay para typing
        await new Promise(resolve => setTimeout(resolve, 800));
        
        hideTyping();
        
        // Agregar respuesta del bot
        if (response.error) {
            addMessage(response.response || 'Lo siento, hubo un error. Intenta de nuevo.');
        } else {
            addMessage(response.response);
            
            // Si hay URL de WhatsApp, agregar botón
            if (response.whatsapp_url) {
                addWhatsAppButton(response.whatsapp_url);
            }
        }
        
    } catch (error) {
        hideTyping();
        addMessage('Lo siento, no pude procesar tu mensaje. Por favor intenta de nuevo.');
        console.error('Error:', error);
    }
}

// Agregar botón de WhatsApp
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

// Mensajes de ejemplo para demostración
const exampleResponses = [
    '¡Gracias por tu mensaje! ¿Podrías contarme más sobre tu proyecto?',
    'Entiendo. ¿Cuál es tu presupuesto aproximado para este proyecto?',
    'Perfecto. ¿Cuándo te gustaría comenzar con la implementación?',
    '¿Eres tú quien toma las decisiones en tu empresa o necesitas consultar con alguien más?',
    'Excelente información. He calificado tu lead con una puntuación alta. Un representante se pondrá en contacto contigo pronto.'
];

let exampleIndex = 0;

// Agregar respuesta de ejemplo para demo
function addExampleResponse() {
    if (exampleIndex < exampleResponses.length) {
        setTimeout(() => {
            hideTyping();
            addMessage(exampleResponses[exampleIndex]);
            exampleIndex++;
        }, 1000 + Math.random() * 1000);
    } else {
        setTimeout(() => {
            hideTyping();
            addMessage('Gracias por la conversación. ¿Hay algo más en lo que pueda ayudarte?');
            exampleIndex = 0;
        }, 1000);
    }
}

// Event Listeners
chatbotToggle.addEventListener('click', toggleChatbot);
chatbotClose.addEventListener('click', toggleChatbot);

chatbotSend.addEventListener('click', sendMessage);

chatbotInputField.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Prevenir que el input pierda foco al hacer click en enviar
chatbotSend.addEventListener('mousedown', (e) => {
    e.preventDefault();
});

// Inicialización
console.log('Chatbot Widget inicializado');
console.log('Session ID:', chatbotAPI.sessionId);

// Mostrar notificación inicial después de 3 segundos
setTimeout(() => {
    if (!isOpen) {
        messageCount = 1;
        updateBadge();
    }
}, 3000);