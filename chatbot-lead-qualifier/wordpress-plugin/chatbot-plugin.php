<?php
/**
 * Plugin Name: Sparks IoT & Energy Chatbot
 * Plugin URI: https://sparksenergy.io
 * Description: Chatbot inteligente de atención al cliente para Sparks IoT & Energy. Genera leads cualificados y proporciona información sobre servicios de energías renovables.
 * Version: 1.0.0
 * Author: Sparks IoT & Energy
 * Author URI: https://sparksenergy.io
 * License: GPL v2 or later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: sparks-chatbot
 * Domain Path: /languages
 */

// Evitar acceso directo
if (!defined('ABSPATH')) {
    exit;
}

// Definir constantes del plugin
define('SPARKS_CHATBOT_VERSION', '1.0.0');
define('SPARKS_CHATBOT_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('SPARKS_CHATBOT_PLUGIN_URL', plugin_dir_url(__FILE__));
define('SPARKS_CHATBOT_PLUGIN_BASENAME', plugin_basename(__FILE__));

/**
 * Clase principal del plugin
 */
class Sparks_Chatbot_Plugin {
    
    /**
     * Instancia única del plugin
     */
    private static $instance = null;
    
    /**
     * URL de la API del chatbot
     */
    private $api_url;
    
    /**
     * Constructor
     */
    private function __construct() {
        $this->api_url = get_option('sparks_chatbot_api_url', 'http://127.0.0.1:5000/api');
        $this->init_hooks();
    }
    
    /**
     * Obtener instancia única (Singleton)
     */
    public static function get_instance() {
        if (null === self::$instance) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    /**
     * Inicializar hooks de WordPress
     */
    private function init_hooks() {
        // Activación y desactivación
        register_activation_hook(__FILE__, array($this, 'activate'));
        register_deactivation_hook(__FILE__, array($this, 'deactivate'));
        
        // Acciones de WordPress
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_action('wp_footer', array($this, 'render_chatbot_widget'));
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_init', array($this, 'register_settings'));
        
        // Shortcode
        add_shortcode('sparks_chatbot', array($this, 'chatbot_shortcode'));
        
        // AJAX endpoints
        add_action('wp_ajax_sparks_chatbot_message', array($this, 'handle_chat_message'));
        add_action('wp_ajax_nopriv_sparks_chatbot_message', array($this, 'handle_chat_message'));
    }
    
    /**
     * Activación del plugin
     */
    public function activate() {
        // Configuración por defecto
        add_option('sparks_chatbot_enabled', '1');
        add_option('sparks_chatbot_api_url', 'http://127.0.0.1:5000/api');
        add_option('sparks_chatbot_position', 'bottom-right');
        add_option('sparks_chatbot_color', '#2563eb');
        add_option('sparks_chatbot_title', 'Sparks IoT & Energy');
        add_option('sparks_chatbot_subtitle', 'Chatbot de atención al cliente');
        add_option('sparks_chatbot_welcome_message', '¡Hola! ¿En qué puedo ayudarte hoy?');
        
        flush_rewrite_rules();
    }
    
    /**
     * Desactivación del plugin
     */
    public function deactivate() {
        flush_rewrite_rules();
    }
    
    /**
     * Cargar scripts y estilos
     */
    public function enqueue_scripts() {
        if (!$this->is_chatbot_enabled()) {
            return;
        }
        
        // CSS del chatbot
        wp_enqueue_style(
            'sparks-chatbot-styles',
            SPARKS_CHATBOT_PLUGIN_URL . 'assets/css/chatbot.css',
            array(),
            SPARKS_CHATBOT_VERSION
        );
        
        // JavaScript del chatbot
        wp_enqueue_script(
            'sparks-chatbot-script',
            SPARKS_CHATBOT_PLUGIN_URL . 'assets/js/chatbot.js',
            array('jquery'),
            SPARKS_CHATBOT_VERSION,
            true
        );
        
        // Pasar variables de PHP a JavaScript
        wp_localize_script('sparks-chatbot-script', 'sparksChatbot', array(
            'ajaxUrl' => admin_url('admin-ajax.php'),
            'apiUrl' => $this->api_url,
            'nonce' => wp_create_nonce('sparks_chatbot_nonce'),
            'settings' => array(
                'title' => get_option('sparks_chatbot_title', 'Sparks IoT & Energy'),
                'subtitle' => get_option('sparks_chatbot_subtitle', 'Chatbot de atención al cliente'),
                'welcomeMessage' => get_option('sparks_chatbot_welcome_message', '¡Hola! ¿En qué puedo ayudarte hoy?'),
                'position' => get_option('sparks_chatbot_position', 'bottom-right'),
                'color' => get_option('sparks_chatbot_color', '#2563eb')
            )
        ));
    }
    
    /**
     * Renderizar widget del chatbot
     */
    public function render_chatbot_widget() {
        if (!$this->is_chatbot_enabled()) {
            return;
        }
        
        include SPARKS_CHATBOT_PLUGIN_DIR . 'templates/chatbot-widget.php';
    }
    
    /**
     * Shortcode del chatbot
     */
    public function chatbot_shortcode($atts) {
        $atts = shortcode_atts(array(
            'inline' => 'false',
            'height' => '600px'
        ), $atts);
        
        ob_start();
        include SPARKS_CHATBOT_PLUGIN_DIR . 'templates/chatbot-inline.php';
        return ob_get_clean();
    }
    
    /**
     * Manejar mensajes del chat vía AJAX
     */
    public function handle_chat_message() {
        // Verificar nonce
        check_ajax_referer('sparks_chatbot_nonce', 'nonce');
        
        $message = sanitize_text_field($_POST['message']);
        $session_id = sanitize_text_field($_POST['session_id']);
        
        // Hacer petición a la API del chatbot
        $response = wp_remote_post($this->api_url . '/chat', array(
            'headers' => array('Content-Type' => 'application/json'),
            'body' => json_encode(array(
                'message' => $message,
                'session_id' => $session_id
            )),
            'timeout' => 30
        ));
        
        if (is_wp_error($response)) {
            wp_send_json_error(array(
                'message' => 'Error al conectar con el chatbot'
            ));
        }
        
        $body = wp_remote_retrieve_body($response);
        $data = json_decode($body, true);
        
        wp_send_json_success($data);
    }
    
    /**
     * Agregar menú de administración
     */
    public function add_admin_menu() {
        add_options_page(
            'Configuración del Chatbot',
            'Chatbot Sparks',
            'manage_options',
            'sparks-chatbot-settings',
            array($this, 'render_admin_page')
        );
    }
    
    /**
     * Registrar configuraciones
     */
    public function register_settings() {
        register_setting('sparks_chatbot_settings', 'sparks_chatbot_enabled');
        register_setting('sparks_chatbot_settings', 'sparks_chatbot_api_url');
        register_setting('sparks_chatbot_settings', 'sparks_chatbot_position');
        register_setting('sparks_chatbot_settings', 'sparks_chatbot_color');
        register_setting('sparks_chatbot_settings', 'sparks_chatbot_title');
        register_setting('sparks_chatbot_settings', 'sparks_chatbot_subtitle');
        register_setting('sparks_chatbot_settings', 'sparks_chatbot_welcome_message');
    }
    
    /**
     * Renderizar página de administración
     */
    public function render_admin_page() {
        include SPARKS_CHATBOT_PLUGIN_DIR . 'templates/admin-settings.php';
    }
    
    /**
     * Verificar si el chatbot está habilitado
     */
    private function is_chatbot_enabled() {
        return get_option('sparks_chatbot_enabled', '1') === '1';
    }
}

// Inicializar el plugin
function sparks_chatbot_init() {
    return Sparks_Chatbot_Plugin::get_instance();
}

// Ejecutar cuando WordPress esté listo
add_action('plugins_loaded', 'sparks_chatbot_init');

