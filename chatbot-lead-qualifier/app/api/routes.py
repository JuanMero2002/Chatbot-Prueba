# Routes API
from flask import Blueprint, request, jsonify
from app.utils.logger import setup_logger
from datetime import datetime
import re
import json
import os

logger = setup_logger(__name__)

api_bp = Blueprint('api', __name__)

# Almacenamiento temporal de sesiones (en producción usar Redis o DB)
sessions = {}

# Cargar base de conocimiento
KB_PATH = os.path.join(os.path.dirname(__file__), '..', 'chatbot', 'knowledge_base.json')
try:
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        KNOWLEDGE_BASE = json.load(f)
    logger.info('Base de conocimiento cargada exitosamente')
except Exception as e:
    logger.error(f'Error cargando knowledge_base.json: {e}')
    KNOWLEDGE_BASE = {}

# Servicios disponibles (cargados de knowledge_base)
def obtener_servicios():
    """Obtiene los servicios de la base de conocimiento"""
    return KNOWLEDGE_BASE.get('servicios', {})

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
    if any(word in mensaje for word in ['hola', 'buenos', 'buenas', 'saludos', 'hey', 'hi', 'buenos dias', 'buenas tardes']):
        return 'saludo'
    
    # Información sobre proyectos/experiencia
    if any(word in mensaje for word in ['proyecto', 'experiencia', 'casos', 'referencias', 'ejemplo', 'hicieron', 'realizaron', 'cartera']):
        return 'consulta_proyectos'
    
    # Certificaciones/ISO
    if any(word in mensaje for word in ['certificacion', 'iso', 'norma', 'estandar']):
        return 'consulta_certificaciones'
    
    # Información sobre marcas/equipos
    if any(word in mensaje for word in ['marca', 'inversor', 'equipo', 'panel', 'bateria', 'tecnologia', 'especif']):
        return 'consulta_marcas'
    
    # Precio/Cotización (ANTES que servicios para mayor especificidad)
    if any(word in mensaje for word in ['precio', 'costo', 'cotizacion', 'cuanto', 'valor', 'inversion', 'presupuesto']):
        return 'precio'
    
    # Interés en servicios
    if any(word in mensaje for word in ['servicio', 'ofrecen', 'tienen', 'hacen', 'producto', 'ofrecer']):
        return 'consulta_servicios'
    
    # Información general
    if any(word in mensaje for word in ['informacion', 'info', 'sobre', 'acerca', 'que es', 'quienes son', 'empresa']):
        return 'info_general'
    
    # Contacto
    if any(word in mensaje for word in ['contacto', 'llamar', 'telefono', 'whatsapp', 'escribir', 'contactarme']):
        return 'contacto'
    
    # Confirmación positiva
    if any(word in mensaje for word in ['si', 'sí', 'claro', 'ok', 'dale', 'quiero', 'deseo', 'me interesa', 'afirmativo', 'si please', 'aceptar']):
        return 'confirmacion_si'
    
    # Negación
    if any(word in mensaje for word in ['no', 'nada', 'gracias', 'negativo', 'no gracias']):
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
    mensaje = f"Hola Sparks IoT&Energy, soy {usuario} y deseo información sobre {servicio_nombre}"
    # Usar número de WhatsApp de la empresa desde knowledge_base
    contacto = KNOWLEDGE_BASE.get('contacto', {})
    whatsapp_numeros = contacto.get('whatsapp', ['+593 982840675'])
    numero = whatsapp_numeros[0].replace('+', '').replace(' ', '')
    url_whatsapp = f"https://wa.me/{numero}?text={mensaje.replace(' ', '%20')}"
    return url_whatsapp

def obtener_contacto_empresa():
    """Obtiene información de contacto desde la base de conocimiento"""
    return KNOWLEDGE_BASE.get('contacto', {})

def obtener_informacion_empresa():
    """Obtiene información corporativa desde la base de conocimiento"""
    return KNOWLEDGE_BASE.get('empresa', {})

def obtener_proyectos_referencia():
    """Obtiene los proyectos de referencia para generar confianza"""
    return KNOWLEDGE_BASE.get('proyectos_realizados', {})

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
            empresa = obtener_informacion_empresa()
            response_text = f"""🌍 **Sobre {empresa.get('nombre_oficial', 'Sparks IoT&Energy')}**

{empresa.get('descripcion', 'Soluciones tecnológicas para ciudades inteligentes y sostenibles.')}

**Ubicación:** {empresa.get('ubicacion_principal', {}).get('nombre', '')}, Manta, Ecuador

**Nuestra Misión:**
{empresa.get('mision', '')}

**Nuestra Visión:**
{empresa.get('vision', '')}

**Nuestro Posicionamiento:**
Somos tu {empresa.get('posicionamiento', 'aliado estratégico')} en la transición energética.

¿Te gustaría conocer nuestros servicios específicos o projectos de referencia?"""
            sesion['estado'] = 'presentacion'
        
        elif intencion == 'consulta_proyectos':
            proyectos = obtener_proyectos_referencia()
            response_text = """📁 **Nuestros Proyectos de Referencia**

Contamos con una cartera de proyectos exitosos en tres sectores:

🏠 **Residencial:**
• Urbanización Barú (Manta): Sistema On-Grid 5 kW
• Ciudad del Mar (Manta): Sistema On-Grid 10 kW + Sistema Híbrido 5 kW

🏢 **Comercial:**
• Motel Intimus (Jipijapa): Sistema solar 22 kW (40 paneles)
• Multiservicios Julio (Manta): Sistema 15 kW

🏛️ **Público y Comunitario:**
• EPAM Manta: Infraestructura fotovoltaica en 8 puntos estratégicos
• Comuna Liguiqui: Sistema de Bombeo Solar (abastece a 700m) + Sistema Off-Grid para videovigilancia

Estos proyectos demuestran nuestra experiencia y confiabilidad. ¿Te gustaría saber más sobre alguno en particular?"""
            sesion['estado'] = 'mostrando_proyectos'
        
        elif intencion == 'consulta_certificaciones':
            response_text = """✅ **Nuestras Certificaciones y Estándares**

**ISO 50001 - Gestión de la Energía**
No solo la cumplimos, sino que ofrecemos:
• Consultoría e implementación de ISO 50001
• Auditorías energéticas completas
• Certificación para empresas que busquen acreditar su eficiencia energética

**Normativa ARCONEL**
Cumplimiento de regulaciones locales ecuatorianas para sistemas conectados a red (On-Grid).

**Estándares de Calidad**
Trabajamos con equipos de primera calidad y garantía completa, probados en múltiples proyectos.

¿Deseas información sobre cómo podríamos ayudarte con eficiencia energética o certificaciones?"""
            sesion['estado'] = 'presentacion'
        
        elif intencion == 'consulta_marcas':
            response_text = f"""🔧 **Marcas y Tecnología Utilizada**

Trabajamos con **marcas líderes del mercado** probadas en nuestros proyectos:
✓ **JinkoSolar** - Paneles de alta eficiencia
✓ **SIEMENS** - Sistemas de automatización
✓ **INVT** - Variadores de frecuencia
✓ **GROOWATT** - Inversores solares

**Tecnología:**
☀️ **Paneles Monocristalinos** para máxima eficiencia
⚡ **Inversores** On-Grid, Off-Grid e Híbridos
🔋 **Almacenamiento:** Baterías de Litio (larga duración) y GEL (aplicaciones rurales)
🏭 **Sistemas PLC y SCADA** para control industrial
📊 **IoT:** Estación Sparks-AQ1 para monitoreo de aire y parámetros ambientales

Para detalles técnicos específicos de tu proyecto, consulta directamente con nuestros ingenieros vía WhatsApp.

¿Cuál servicio te interesa?"""
            sesion['estado'] = 'mostrando_servicios'
        
        elif intencion == 'precio':
            response_text = """💰 **Sobre Precios y Cotización**

Los costos varían según:
• Tipo de instalación (On-Grid, Off-Grid, Híbrida)
• Capacidad requerida (kW)
• Características del sitio
• Componentes seleccionados (paneles, inversores, baterías)
• Ubicación geográfica

**Nuestro Proceso:**
1️⃣ Estudio energético integral (SIN COSTO)
2️⃣ Análisis de tu patrón de consumo
3️⃣ Proyección económica del ahorro
4️⃣ Cotización personalizada
5️⃣ Opciones de financiación

¿Te gustaría agendar una asesoría técnica gratuita?"""
            sesion['estado'] = 'ofreciendo_asesoria'
        
        elif intencion == 'contacto':
            contacto = obtener_contacto_empresa()
            whatsapp_numeros = contacto.get('whatsapp', [])
            numero_whatsapp_principal = whatsapp_numeros[0].replace('+', '').replace(' ', '') if whatsapp_numeros else ''
            
            # Crear URL de WhatsApp directo
            mensaje_whatsapp = "Hola Sparks IoT&Energy, me gustaría recibir información sobre sus servicios"
            if numero_whatsapp_principal:
                whatsapp_url = f"https://wa.me/{numero_whatsapp_principal}?text={mensaje_whatsapp.replace(' ', '%20')}"
            
            response_text = f"""📞 **Nuestros Canales de Contacto**

**WhatsApp (Directo):**
{' | '.join(whatsapp_numeros)}

🔗 **Abrir WhatsApp Directo:**
Toca el botón de abajo para chatear con nosotros en WhatsApp

**Correo Electrónico:**
{contacto.get('correo', 'info@sparksenergy.io')}

**Horario de Atención:**
{contacto.get('horario', 'Lunes a Sábado, 08:00 AM – 08:00 PM')}

**Ubicación:**
Edificio Manta Business Center, Torre B, Piso 3, Oficina 301
Av. Malecón (Frente al Mall del Pacífico), Manta, Manabí, Ecuador

¿Prefieres abrir WhatsApp ahora para una consulta rápida?"""
            sesion['estado'] = 'mostrando_contacto'
        
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