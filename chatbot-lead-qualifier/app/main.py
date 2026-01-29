# App principal
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import Config
from app.api.routes import api_bp
from app.utils.logger import setup_logger
import os

logger = setup_logger(__name__)

def create_app(config_class=Config):
    """Factory para crear la aplicación Flask"""
    # Configurar el directorio de templates y static
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    app = Flask(__name__, 
                static_folder=frontend_dir,
                static_url_path='')
    app.config.from_object(config_class)
    
    # Configurar CORS
    CORS(app, resources={r"/api/*": {"origins": config_class.CORS_ORIGINS}})
    
    # Configurar Rate Limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[config_class.RATELIMIT_DEFAULT],
        storage_uri=config_class.RATELIMIT_STORAGE_URL
    )
    
    # Registrar blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Ruta principal para servir el frontend
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')
    
    # Rutas para archivos estáticos
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)
    
    # Ruta de health check
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'})
    
    # Manejadores de errores
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal error: {error}')
        return jsonify({'error': 'Internal server error'}), 500
    
    logger.info('Aplicación Flask creada exitosamente')
    return app

# Crear instancia de la app
app = create_app()