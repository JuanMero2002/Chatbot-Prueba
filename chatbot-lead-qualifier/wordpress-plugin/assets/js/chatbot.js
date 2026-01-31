/**
 * JavaScript del Chatbot Sparks IoT & Energy para WordPress
 * Version: 1.0.0
 */

(function($) {
    'use strict';

    class SparksChatbot {
        constructor() {
            this.sessionId = this.generateSessionId();
            this.messagesContainer = null;
            this.inputField = null;
            this.form = null;
            this.isOpen = false;
            
            this.init();
        }

        /**
         * Inicializar el chatbot
         */
        init() {
            this.cacheDOMElements();
            this.attachEventListeners();
            this.loadSessionFromStorage();
        }

        /**
         * Cachear elementos del DOM
         */
        cacheDOMElements() {
            this.$toggle = $('#sparks-chatbot-toggle');
            this.$window = $('#sparks-chatbot-window');
            this.$close = $('.sparks-chatbot-close');
            this.messagesContainer = document.getElementById('sparks-chatbot-messages');
            this.inputField = document.getElementById('sparks-chatbot-input');
            this.form = document.getElementById('sparks-chatbot-form');
            this.$typing = $('#sparks-chatbot-typing');
            this.$badge = $('.sparks-chatbot-badge');
        }

        /**
         * Adjuntar event listeners
         */
        attachEventListeners() {
            // Toggle chatbot
            this.$toggle.on('click', () => this.toggleChatbot());
            this.$close.on('click', () => this.closeChatbot());
            
            // Enviar mensaje
            $(this.form).on('submit', (e) => {
                e.preventDefault();
                this.sendMessage();
            });

            // Detectar clicks en botones de WhatsApp
            $(this.messagesContainer).on('click', '.sparks-chatbot-whatsapp-button', function(e) {
                e.preventDefault();
                const url = $(this).attr('href');
                window.open(url, '_blank');
            });
        }

        /**
         * Generar ID de sesión único
         */
        generateSessionId() {
            const stored = localStorage.getItem('sparks_chatbot_session_id');
            if (stored) {
                return stored;
            }
            
            const sessionId = 'wp_session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('sparks_chatbot_session_id', sessionId);
            return sessionId;
        }

        /**
         * Toggle del chatbot
         */
        toggleChatbot() {
            if (this.isOpen) {
                this.closeChatbot();
            } else {
                this.openChatbot();
            }
        }

        /**
         * Abrir chatbot
         */
        openChatbot() {
            this.$window.fadeIn(300);
            this.isOpen = true;
            this.$badge.hide();
            $('.sparks-chatbot-icon-open').hide();
            $('.sparks-chatbot-icon-close').show();
            this.inputField.focus();
            this.scrollToBottom();
        }

        /**
         * Cerrar chatbot
         */
        closeChatbot() {
            this.$window.fadeOut(300);
            this.isOpen = false;
            $('.sparks-chatbot-icon-open').show();
            $('.sparks-chatbot-icon-close').hide();
        }

        /**
         * Enviar mensaje
         */
        async sendMessage() {
            const message = this.inputField.value.trim();
            
            if (!message) {
                return;
            }

            // Agregar mensaje del usuario
            this.addMessage(message, 'user');
            this.inputField.value = '';
            this.scrollToBottom();

            // Mostrar indicador de escritura
            this.$typing.show();

            try {
                // Hacer petición AJAX a WordPress
                const response = await $.ajax({
                    url: sparksChatbot.ajaxUrl,
                    method: 'POST',
                    data: {
                        action: 'sparks_chatbot_message',
                        nonce: sparksChatbot.nonce,
                        message: message,
                        session_id: this.sessionId
                    }
                });

                this.$typing.hide();

                if (response.success && response.data) {
                    const botMessage = response.data.response;
                    const whatsappUrl = response.data.whatsapp_url;
                    
                    this.addMessage(botMessage, 'bot', whatsappUrl);
                    this.saveMessageToStorage(message, 'user');
                    this.saveMessageToStorage(botMessage, 'bot');
                } else {
                    this.addMessage('Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente.', 'bot');
                }
            } catch (error) {
                this.$typing.hide();
                console.error('Error en chatbot:', error);
                this.addMessage('Lo siento, no pude conectarme con el servidor. Por favor, verifica tu conexión.', 'bot');
            }

            this.scrollToBottom();
        }

        /**
         * Agregar mensaje al chat
         */
        addMessage(text, type, whatsappUrl = null) {
            const time = new Date().toLocaleTimeString('es-EC', { hour: '2-digit', minute: '2-digit' });
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `sparks-chatbot-message sparks-chatbot-message-${type}`;
            
            let content = `
                <div class="sparks-chatbot-message-content">${this.escapeHtml(text)}</div>
                <div class="sparks-chatbot-message-time">${time}</div>
            `;

            // Agregar botón de WhatsApp si existe URL
            if (whatsappUrl && type === 'bot') {
                content += `
                    <a href="${whatsappUrl}" class="sparks-chatbot-whatsapp-button" target="_blank" rel="noopener">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                        </svg>
                        Contactar por WhatsApp
                    </a>
                `;
            }

            messageDiv.innerHTML = content;
            this.messagesContainer.appendChild(messageDiv);
        }

        /**
         * Scroll al final del chat
         */
        scrollToBottom() {
            setTimeout(() => {
                this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
            }, 100);
        }

        /**
         * Escapar HTML
         */
        escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML.replace(/\n/g, '<br>');
        }

        /**
         * Guardar mensaje en localStorage
         */
        saveMessageToStorage(text, type) {
            try {
                const messages = JSON.parse(localStorage.getItem('sparks_chatbot_messages') || '[]');
                messages.push({
                    text: text,
                    type: type,
                    timestamp: Date.now()
                });
                
                // Mantener solo los últimos 50 mensajes
                if (messages.length > 50) {
                    messages.splice(0, messages.length - 50);
                }
                
                localStorage.setItem('sparks_chatbot_messages', JSON.stringify(messages));
            } catch (error) {
                console.error('Error guardando mensajes:', error);
            }
        }

        /**
         * Cargar sesión desde localStorage
         */
        loadSessionFromStorage() {
            try {
                const messages = JSON.parse(localStorage.getItem('sparks_chatbot_messages') || '[]');
                
                // Cargar mensajes de las últimas 24 horas
                const oneDayAgo = Date.now() - (24 * 60 * 60 * 1000);
                const recentMessages = messages.filter(msg => msg.timestamp > oneDayAgo);
                
                if (recentMessages.length > 1) { // Solo si hay más del mensaje de bienvenida
                    // Limpiar mensajes actuales excepto el de bienvenida
                    this.messagesContainer.innerHTML = '';
                    
                    // Reagregar mensajes recientes
                    recentMessages.forEach(msg => {
                        this.addMessage(msg.text, msg.type);
                    });
                }
            } catch (error) {
                console.error('Error cargando sesión:', error);
            }
        }
    }

    // Inicializar cuando el DOM esté listo
    $(document).ready(function() {
        new SparksChatbot();
    });

})(jQuery);
