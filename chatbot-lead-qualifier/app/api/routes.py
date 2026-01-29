# Routes API
from flask import Blueprint, request, jsonify
from app.utils.logger import setup_logger
from datetime import datetime
import re

logger = setup_logger(__name__)

api_bp = Blueprint('api', __name__)

# Almacenamiento temporal de sesiones (en producción usar Redis o DB)
sessions = {}

# Servicios disponibles
SERVICIOS = {
    'solar_aislada': {
        'nombre': 'Solar Fotovoltaica o Híbrida Aislada (Off-grid)',
        'descripcion': 'Instalación solar que genera energía sin conexión a red. Ideal para zonas rurales con autonomía completa mediante baterías.',
        'keywords': ['aislada', 'off-grid', 'sin red', 'autonoma', 'bateria', 'rural', 'remota']
    },
    'solar_red': {
        'nombre': 'Solar Fotovoltaica Conectada a Red (On-Grid)',
        'descripcion': 'Sistema conectado a red que permite generar tu propia energía e inyectar excedentes. Reduce tu factura eléctrica hasta alcanzar balance cero.',
        'keywords': ['conectada', 'on-grid', 'red', 'factura', 'ahorro', 'excedente']
    },
    'bombeo': {
        'nombre': 'Sistemas de Bombeo Solar',
        'descripcion': 'Bombeo o riego fotovoltaico que reduce costos de electricidad. Optimizado con variadores de frecuencia para máximo rendimiento.',
        'keywords': ['bombeo', 'riego', 'agua', 'agricultura', 'pozo']
    },
    'iluminacion': {
        'nombre': 'Sistemas de Iluminación Solar',
        'descripcion': 'Iluminación LED solar para espacios públicos y privados. Ideal para parques, calles, emergencias con sensores de presencia.',
        'keywords': ['iluminacion', 'luz', 'led', 'calle', 'parque', 'emergencia']
    },
    'eficiencia': {
        'nombre': 'Eficiencia Energética',
        'descripcion': 'Optimización de tu consumo energético mediante auditorías y soluciones personalizadas para reducir costos.',
        'keywords': ['eficiencia', 'optimizar', 'consumo', 'auditoria', 'reducir']
    },
    'industria': {
        'nombre': 'Industria 4.0',
        'descripcion': 'Automatización de procesos industriales con IoT y tecnologías inteligentes para mayor eficiencia.',
        'keywords': ['industria', 'automatizacion', 'iot', 'procesos', '4.0']
    }
}

def detectar_intencion(mensaje):
    """Detecta la intención del usuario"""
    mensaje = mensaje.lower()
    
    # Saludos
    if any(word in mensaje for word in ['hola', 'buenos', 'buenas', 'saludos', 'hey', 'hi']):
        return 'saludo'
    
    # Interés en servicios
    if any(word in mensaje for word in ['servicio', 'ofrecen', 'tienen', 'hacen', 'producto']):
        return 'consulta_servicios'
    
    # Información general
    if any(word in mensaje for word in ['informacion', 'info', 'sobre', 'acerca', 'que es']):
        return 'info_general'
    
    # Precio/Cotización
    if any(word in mensaje for word in ['precio', 'costo', 'cotizacion', 'cuanto', 'valor']):
        return 'precio'
    
    # Contacto
    if any(word in mensaje for word in ['contacto', 'llamar', 'telefono', 'whatsapp', 'escribir']):
        return 'contacto'
    
    # Confirmación positiva
    if any(word in mensaje for word in ['si', 'sí', 'claro', 'ok', 'dale', 'quiero', 'deseo', 'me interesa', 'afirmativo']):
        return 'confirmacion_si'
    
    # Negación
    if any(word in mensaje for word in ['no', 'nada', 'gracias', 'negativo']):
        return 'confirmacion_no'
    
    # Detectar servicio específico
    for servicio_key, servicio in SERVICIOS.items():
        if any(keyword in mensaje for keyword in servicio['keywords']):
            return f'servicio_{servicio_key}'
    
    return 'general'

def obtener_sesion(session_id):
    """Obtiene o crea una sesión"""
    if session_id not in sessions:
        sessions[session_id] = {
            'estado': 'inicial',
            'servicio_interes': None,
            'mensajes': [],
            'datos_usuario': {}
        }
    return sessions[session_id]

def generar_mensaje_whatsapp(usuario, servicio_nombre):
    """Genera el mensaje pre-formateado para WhatsApp"""
    mensaje = f"Hola, soy {usuario} y deseo información sobre {servicio_nombre}"
    # Número de WhatsApp de la empresa (actualizar con el real)
    numero_whatsapp = "593999999999"  # Cambiar por el número real
    url_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensaje.replace(' ', '%20')}"
    return url_whatsapp

@api_bp.route('/chat', methods=['POST'])
def chat():
    """Endpoint principal para conversación con el chatbot"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Se requiere un mensaje'}), 400
        
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default-session')
        
        logger.info(f'Mensaje recibido: {user_message[:50]}... | Session: {session_id}')
        
        # Obtener sesión
        sesion = obtener_sesion(session_id)
        sesion['mensajes'].append({'tipo': 'usuario', 'texto': user_message})
        
        # Detectar intención
        intencion = detectar_intencion(user_message)
        logger.info(f'Intención detectada: {intencion}')
        
        response_text = ''
        whatsapp_url = None
        
        # Manejo de estados y respuestas
        if intencion == 'saludo':
            response_text = """¡Hola! 👋 Bienvenido a Sparks IoT&Energy.

🌱 Trabajamos por un mejor futuro para nuestro planeta a través de energías renovables en Manta, Manabí, Ecuador.

Nuestros servicios principales:
🔹 Eficiencia Energética
🔹 Energías Renovables
🔹 Industria 4.0

¿En qué puedo ayudarte hoy?"""
            sesion['estado'] = 'presentacion'
        
        elif intencion == 'consulta_servicios':
            response_text = """Excelente! Te cuento sobre nuestros servicios de energías renovables:

☀️ **Solar Fotovoltaica Aislada (Off-Grid)**
Sistemas autónomos sin conexión a red, ideales para zonas rurales.

⚡ **Solar Fotovoltaica Conectada a Red (On-Grid)**
Genera tu propia energía y reduce tu factura eléctrica.

💧 **Sistemas de Bombeo Solar**
Soluciones para riego y bombeo de agua optimizadas.

💡 **Sistemas de Iluminación Solar**
Iluminación LED para espacios públicos y privados.

📊 **Eficiencia Energética**
Auditorías y optimización de consumo.

🏭 **Industria 4.0**
Automatización y IoT para procesos industriales.

¿Sobre cuál servicio te gustaría conocer más?"""
            sesion['estado'] = 'mostrando_servicios'
        
        elif intencion.startswith('servicio_'):
            servicio_key = intencion.replace('servicio_', '')
            if servicio_key in SERVICIOS:
                servicio = SERVICIOS[servicio_key]
                sesion['servicio_interes'] = servicio_key
                sesion['estado'] = 'esperando_confirmacion'
                
                response_text = f"""📌 **{servicio['nombre']}**

{servicio['descripcion']}

✅ Realizamos:
• Estudio energético integral
• Visitas técnicas
• Medición de patrones de consumo
• Proyección económica del ahorro
• Financiación y tramitación
• Instalación y seguimiento

¿Te gustaría que un asesor técnico se comunique contigo para brindarte más información sobre este servicio?"""
        
        elif intencion == 'confirmacion_si' and sesion['estado'] == 'esperando_confirmacion':
            servicio_key = sesion.get('servicio_interes')
            if servicio_key:
                servicio = SERVICIOS[servicio_key]
                # Extraer posible nombre del usuario de mensajes anteriores
                usuario = "Cliente"
                
                whatsapp_url = generar_mensaje_whatsapp(usuario, servicio['nombre'])
                
                response_text = f"""¡Perfecto! 🎉

Para brindarte la mejor atención personalizada, te invito a continuar la conversación por WhatsApp.

He preparado un mensaje para ti sobre: **{servicio['nombre']}**

¿Deseas abrir WhatsApp ahora?"""
                sesion['estado'] = 'redirigiendo_whatsapp'
            else:
                response_text = "Por favor, dime sobre qué servicio te gustaría recibir información."
        
        elif intencion == 'confirmacion_no' and sesion['estado'] == 'esperando_confirmacion':
            response_text = "No hay problema. ¿Hay algún otro servicio sobre el que quieras conocer más? O si prefieres, puedo contarte sobre cómo funcionamos."
            sesion['estado'] = 'mostrando_servicios'
        
        elif intencion == 'info_general':
            response_text = """🌍 **Sobre Sparks IoT&Energy**

Somos una empresa comprometida con construir un mejor futuro mediante:

♻️ Energía solar fotovoltaica, solar térmica y mini eólica
🌱 Reducción de emisiones de CO2
💰 Ahorro en costos de energía eléctrica
⚡ Promoción de soberanía energética

**¿Cómo funcionamos?**
1️⃣ Estudio energético completo
2️⃣ Financiación y tramitación
3️⃣ Instalación y seguimiento

¿Te gustaría conocer nuestros servicios específicos?"""
            sesion['estado'] = 'presentacion'
        
        elif intencion == 'precio':
            response_text = """Los costos varían según:
• Tipo de instalación
• Capacidad requerida
• Ubicación y características del sitio
• Componentes seleccionados

Para darte una cotización precisa, necesitamos realizar un estudio energético integral sin costo.

¿Te gustaría agendar una asesoría técnica gratuita?"""
            sesion['estado'] = 'ofreciendo_asesoria'
        
        elif intencion == 'contacto':
            response_text = """📞 **Contáctanos**

¿Prefieres que te contactemos por WhatsApp?

Dime sobre qué servicio necesitas información y te redirigiré con un asesor especializado."""
            sesion['estado'] = 'mostrando_servicios'
        
        else:
            response_text = """Estoy aquí para ayudarte con información sobre nuestros servicios de energías renovables.

Puedo contarte sobre:
• Instalaciones solares
• Sistemas de bombeo
• Iluminación solar
• Eficiencia energética
• Automatización industrial

¿Qué te interesa saber?"""
        
        # Guardar respuesta
        sesion['mensajes'].append({'tipo': 'bot', 'texto': response_text})
        
        response = {
            'response': response_text,
            'session_id': session_id,
            'intent': intencion,
            'estado': sesion['estado'],
            'timestamp': datetime.now().isoformat()
        }
        
        if whatsapp_url:
            response['whatsapp_url'] = whatsapp_url
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f'Error en /chat: {str(e)}')
        return jsonify({'error': 'Error interno del servidor'}), 500

@api_bp.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Obtener información de una sesión"""
    try:
        return jsonify({
            'session_id': session_id,
            'status': 'active',
            'messages_count': 0
        }), 200
    except Exception as e:
        logger.error(f'Error en /session: {str(e)}')
        return jsonify({'error': 'Error interno del servidor'}), 500

@api_bp.route('/leads', methods=['GET'])
def get_leads():
    """Obtener lista de leads"""
    try:
        return jsonify({
            'leads': [],
            'total': 0
        }), 200
    except Exception as e:
        logger.error(f'Error en /leads: {str(e)}')
        return jsonify({'error': 'Error interno del servidor'}), 500

from datetime import datetime