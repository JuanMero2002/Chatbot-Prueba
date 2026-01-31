<?php
/**
 * Template para chatbot inline (usando shortcode)
 */

if (!defined('ABSPATH')) {
    exit;
}

$height = isset($atts['height']) ? esc_attr($atts['height']) : '600px';
?>

<div class="sparks-chatbot-inline-container" style="max-width: 100%; height: <?php echo $height; ?>;">
    <div class="sparks-chatbot-inline-window" style="height: 100%; display: flex; flex-direction: column; border: 1px solid #e5e7eb; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        
        <!-- Header -->
        <div class="sparks-chatbot-header">
            <div class="sparks-chatbot-header-info">
                <h3 class="sparks-chatbot-title"><?php echo esc_html(get_option('sparks_chatbot_title', 'Sparks IoT & Energy')); ?></h3>
                <p class="sparks-chatbot-subtitle"><?php echo esc_html(get_option('sparks_chatbot_subtitle', 'Chatbot de atención al cliente')); ?></p>
            </div>
        </div>
        
        <!-- Área de mensajes -->
        <div id="sparks-chatbot-messages-inline" class="sparks-chatbot-messages" style="flex: 1; overflow-y: auto; padding: 20px; background: #f9fafb;">
            <div class="sparks-chatbot-message sparks-chatbot-message-bot">
                <div class="sparks-chatbot-message-content">
                    <?php echo esc_html(get_option('sparks_chatbot_welcome_message', '¡Hola! ¿En qué puedo ayudarte hoy?')); ?>
                </div>
                <div class="sparks-chatbot-message-time"><?php echo current_time('H:i'); ?></div>
            </div>
        </div>
        
        <!-- Indicador de escritura -->
        <div id="sparks-chatbot-typing-inline" class="sparks-chatbot-typing" style="display: none;">
            <span></span>
            <span></span>
            <span></span>
        </div>
        
        <!-- Input de mensaje -->
        <div class="sparks-chatbot-input-container">
            <form class="sparks-chatbot-form-inline">
                <input 
                    type="text" 
                    class="sparks-chatbot-input sparks-chatbot-input-inline" 
                    placeholder="Escribe tu mensaje..."
                    autocomplete="off"
                    required
                >
                <button type="submit" class="sparks-chatbot-send" aria-label="Enviar mensaje">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                </button>
            </form>
        </div>
    </div>
</div>

<script>
// Versión simplificada para chatbot inline
jQuery(document).ready(function($) {
    const sessionId = 'wp_inline_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    const $form = $('.sparks-chatbot-form-inline');
    const $input = $('.sparks-chatbot-input-inline');
    const $messages = $('#sparks-chatbot-messages-inline');
    const $typing = $('#sparks-chatbot-typing-inline');
    
    $form.on('submit', function(e) {
        e.preventDefault();
        
        const message = $input.val().trim();
        if (!message) return;
        
        // Agregar mensaje del usuario
        const time = new Date().toLocaleTimeString('es-EC', { hour: '2-digit', minute: '2-digit' });
        $messages.append(`
            <div class="sparks-chatbot-message sparks-chatbot-message-user">
                <div class="sparks-chatbot-message-content">${$('<div>').text(message).html()}</div>
                <div class="sparks-chatbot-message-time">${time}</div>
            </div>
        `);
        
        $input.val('');
        $messages.scrollTop($messages[0].scrollHeight);
        $typing.show();
        
        // Enviar a la API
        $.ajax({
            url: sparksChatbot.ajaxUrl,
            method: 'POST',
            data: {
                action: 'sparks_chatbot_message',
                nonce: sparksChatbot.nonce,
                message: message,
                session_id: sessionId
            },
            success: function(response) {
                $typing.hide();
                
                if (response.success && response.data) {
                    const botMessage = response.data.response;
                    const whatsappUrl = response.data.whatsapp_url;
                    const botTime = new Date().toLocaleTimeString('es-EC', { hour: '2-digit', minute: '2-digit' });
                    
                    let messageHtml = `
                        <div class="sparks-chatbot-message sparks-chatbot-message-bot">
                            <div class="sparks-chatbot-message-content">${$('<div>').text(botMessage).html().replace(/\n/g, '<br>')}</div>
                            <div class="sparks-chatbot-message-time">${botTime}</div>
                    `;
                    
                    if (whatsappUrl) {
                        messageHtml += `
                            <a href="${whatsappUrl}" class="sparks-chatbot-whatsapp-button" target="_blank" rel="noopener">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
                                </svg>
                                Contactar por WhatsApp
                            </a>
                        `;
                    }
                    
                    messageHtml += '</div>';
                    $messages.append(messageHtml);
                } else {
                    $messages.append(`
                        <div class="sparks-chatbot-message sparks-chatbot-message-bot">
                            <div class="sparks-chatbot-message-content">Lo siento, hubo un error. Por favor, intenta nuevamente.</div>
                        </div>
                    `);
                }
                
                $messages.scrollTop($messages[0].scrollHeight);
            },
            error: function() {
                $typing.hide();
                $messages.append(`
                    <div class="sparks-chatbot-message sparks-chatbot-message-bot">
                        <div class="sparks-chatbot-message-content">Lo siento, no pude conectarme con el servidor.</div>
                    </div>
                `);
                $messages.scrollTop($messages[0].scrollHeight);
            }
        });
    });
});
</script>
