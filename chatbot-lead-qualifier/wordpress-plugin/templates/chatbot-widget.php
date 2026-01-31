<?php
/**
 * Template para el widget flotante del chatbot
 */

if (!defined('ABSPATH')) {
    exit;
}
?>

<div id="sparks-chatbot-container" class="sparks-chatbot-<?php echo esc_attr(get_option('sparks_chatbot_position', 'bottom-right')); ?>">
    <!-- Botón flotante -->
    <button id="sparks-chatbot-toggle" class="sparks-chatbot-toggle" aria-label="Abrir chatbot">
        <svg class="sparks-chatbot-icon-open" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
        <svg class="sparks-chatbot-icon-close" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="display: none;">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        <span class="sparks-chatbot-badge">1</span>
    </button>
    
    <!-- Ventana del chat -->
    <div id="sparks-chatbot-window" class="sparks-chatbot-window" style="display: none;">
        <!-- Header -->
        <div class="sparks-chatbot-header">
            <div class="sparks-chatbot-header-info">
                <h3 class="sparks-chatbot-title"><?php echo esc_html(get_option('sparks_chatbot_title', 'Sparks IoT & Energy')); ?></h3>
                <p class="sparks-chatbot-subtitle"><?php echo esc_html(get_option('sparks_chatbot_subtitle', 'Chatbot de atención al cliente')); ?></p>
            </div>
            <button class="sparks-chatbot-close" aria-label="Cerrar chatbot">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
        
        <!-- Área de mensajes -->
        <div id="sparks-chatbot-messages" class="sparks-chatbot-messages">
            <div class="sparks-chatbot-message sparks-chatbot-message-bot">
                <div class="sparks-chatbot-message-content">
                    <?php echo esc_html(get_option('sparks_chatbot_welcome_message', '¡Hola! ¿En qué puedo ayudarte hoy?')); ?>
                </div>
                <div class="sparks-chatbot-message-time"><?php echo current_time('H:i'); ?></div>
            </div>
        </div>
        
        <!-- Indicador de escritura -->
        <div id="sparks-chatbot-typing" class="sparks-chatbot-typing" style="display: none;">
            <span></span>
            <span></span>
            <span></span>
        </div>
        
        <!-- Input de mensaje -->
        <div class="sparks-chatbot-input-container">
            <form id="sparks-chatbot-form">
                <input 
                    type="text" 
                    id="sparks-chatbot-input" 
                    class="sparks-chatbot-input" 
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

<style>
    :root {
        --sparks-chatbot-color: <?php echo esc_attr(get_option('sparks_chatbot_color', '#2563eb')); ?>;
    }
</style>
