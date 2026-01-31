<?php
/**
 * Página de configuración del plugin en el admin de WordPress
 */

if (!defined('ABSPATH')) {
    exit;
}
?>

<div class="wrap">
    <h1>Configuración del Chatbot Sparks IoT & Energy</h1>
    
    <?php settings_errors(); ?>
    
    <form method="post" action="options.php">
        <?php
        settings_fields('sparks_chatbot_settings');
        do_settings_sections('sparks_chatbot_settings');
        ?>
        
        <table class="form-table">
            <tr>
                <th scope="row">
                    <label for="sparks_chatbot_enabled">Habilitar Chatbot</label>
                </th>
                <td>
                    <input type="checkbox" 
                           id="sparks_chatbot_enabled" 
                           name="sparks_chatbot_enabled" 
                           value="1" 
                           <?php checked('1', get_option('sparks_chatbot_enabled', '1')); ?>>
                    <p class="description">Activar o desactivar el chatbot en el sitio web</p>
                </td>
            </tr>
            
            <tr>
                <th scope="row">
                    <label for="sparks_chatbot_api_url">URL de la API</label>
                </th>
                <td>
                    <input type="url" 
                           id="sparks_chatbot_api_url" 
                           name="sparks_chatbot_api_url" 
                           value="<?php echo esc_attr(get_option('sparks_chatbot_api_url', 'http://127.0.0.1:5000/api')); ?>" 
                           class="regular-text"
                           required>
                    <p class="description">URL del servidor de la API del chatbot (ejemplo: http://127.0.0.1:5000/api)</p>
                </td>
            </tr>
            
            <tr>
                <th scope="row">
                    <label for="sparks_chatbot_title">Título del Chatbot</label>
                </th>
                <td>
                    <input type="text" 
                           id="sparks_chatbot_title" 
                           name="sparks_chatbot_title" 
                           value="<?php echo esc_attr(get_option('sparks_chatbot_title', 'Sparks IoT & Energy')); ?>" 
                           class="regular-text">
                </td>
            </tr>
            
            <tr>
                <th scope="row">
                    <label for="sparks_chatbot_subtitle">Subtítulo</label>
                </th>
                <td>
                    <input type="text" 
                           id="sparks_chatbot_subtitle" 
                           name="sparks_chatbot_subtitle" 
                           value="<?php echo esc_attr(get_option('sparks_chatbot_subtitle', 'Chatbot de atención al cliente')); ?>" 
                           class="regular-text">
                </td>
            </tr>
            
            <tr>
                <th scope="row">
                    <label for="sparks_chatbot_welcome_message">Mensaje de Bienvenida</label>
                </th>
                <td>
                    <textarea id="sparks_chatbot_welcome_message" 
                              name="sparks_chatbot_welcome_message" 
                              rows="3" 
                              class="large-text"><?php echo esc_textarea(get_option('sparks_chatbot_welcome_message', '¡Hola! ¿En qué puedo ayudarte hoy?')); ?></textarea>
                </td>
            </tr>
            
            <tr>
                <th scope="row">
                    <label for="sparks_chatbot_position">Posición</label>
                </th>
                <td>
                    <select id="sparks_chatbot_position" name="sparks_chatbot_position">
                        <option value="bottom-right" <?php selected(get_option('sparks_chatbot_position', 'bottom-right'), 'bottom-right'); ?>>Abajo Derecha</option>
                        <option value="bottom-left" <?php selected(get_option('sparks_chatbot_position', 'bottom-right'), 'bottom-left'); ?>>Abajo Izquierda</option>
                    </select>
                    <p class="description">Posición del botón flotante del chatbot</p>
                </td>
            </tr>
            
            <tr>
                <th scope="row">
                    <label for="sparks_chatbot_color">Color Principal</label>
                </th>
                <td>
                    <input type="color" 
                           id="sparks_chatbot_color" 
                           name="sparks_chatbot_color" 
                           value="<?php echo esc_attr(get_option('sparks_chatbot_color', '#2563eb')); ?>">
                    <p class="description">Color del tema del chatbot</p>
                </td>
            </tr>
        </table>
        
        <?php submit_button('Guardar Configuración'); ?>
    </form>
    
    <hr>
    
    <h2>Uso del Shortcode</h2>
    <p>Para insertar el chatbot en una página o entrada, usa el siguiente shortcode:</p>
    <code>[sparks_chatbot]</code>
    
    <h3>Parámetros opcionales:</h3>
    <ul>
        <li><code>[sparks_chatbot inline="true" height="600px"]</code> - Chatbot integrado en la página</li>
    </ul>
    
    <hr>
    
    <h2>Información del Sistema</h2>
    <table class="widefat">
        <tr>
            <td><strong>Versión del Plugin:</strong></td>
            <td><?php echo SPARKS_CHATBOT_VERSION; ?></td>
        </tr>
        <tr>
            <td><strong>Estado de la API:</strong></td>
            <td>
                <?php
                $api_url = get_option('sparks_chatbot_api_url', 'http://127.0.0.1:5000/api');
                $response = wp_remote_get($api_url . '/health');
                if (!is_wp_error($response) && wp_remote_retrieve_response_code($response) === 200) {
                    echo '<span style="color: green;">✓ Conectado</span>';
                } else {
                    echo '<span style="color: red;">✗ No disponible</span>';
                }
                ?>
            </td>
        </tr>
        <tr>
            <td><strong>WordPress Version:</strong></td>
            <td><?php echo get_bloginfo('version'); ?></td>
        </tr>
    </table>
</div>
