"""
API Routes para el chatbot de Sparks IoT & Energy
Maneja las conversaciones y la lógica de negocio del chatbot
"""

from flask import Blueprint, request, jsonify
from app.utils.logger import setup_logger
from datetime import datetime
import re

# Configuración del logger
logger = setup_logger(__name__)

# Crear blueprint para las rutas de la API
api_bp = Blueprint('api', __name__)

# Almacenamiento temporal de sesiones (en producción usar Redis o base de datos)
sessions = {}

# ============================================================================
# CONSTANTES Y CONFIGURACIÓN
# ============================================================================

WHATSAPP_NUMBER = "593985937244"
COMPANY_NAME = "Sparks IoT & Energy"

COMPANY_INFO = {
    'address': 'Edificio Manta Business Center, Torre B, Piso 3, Oficina 301',
    'city': 'Manta – Manabí – Ecuador',
    'phones': ['+593 982840675', '+593 984141479'],
    'whatsapp': '+593 985937244',
    'email': 'info@sparksenergy.io',
    'website': 'sparksenergy.io'
}

# Definición de servicios disponibles
SERVICIOS = {
    'solar_aislada': {
        'nombre': 'Solar Fotovoltaica Off-Grid (Aislada)',
        'descripcion': 'Sistema solar completamente independiente de la red eléctrica con almacenamiento en baterías de litio. Ideal para zonas rurales o donde no llega la red. Autonomía completa con tecnología bifacial y sistemas híbridos disponibles.',
        'keywords': ['aislada', 'off-grid', 'sin red', 'autonoma', 'bateria', 'rural', 'remota', 'litio', 'independiente']
    },
    'solar_red': {
        'nombre': 'Solar Fotovoltaica On-Grid (Conectada a Red)',
        'descripcion': 'Sistema conectado a la red eléctrica que te permite generar tu propia energía limpia e inyectar excedentes. Reduce tu factura hasta alcanzar balance cero con medidor bidireccional y beneficios de la regulación ARCONEL.',
        'keywords': ['conectada', 'on-grid', 'red', 'factura', 'ahorro', 'excedente', 'arconel', 'medidor']
    },
    'solar_hibrido': {
        'nombre': 'Sistema Solar Híbrido',
        'descripcion': 'Combina lo mejor de On-Grid y Off-Grid: conectado a red con respaldo de baterías. Máxima autonomía y seguridad energética ante cortes de luz. Sistemas de 5-10 kWh de almacenamiento en litio.',
        'keywords': ['hibrido', 'híbrido', 'respaldo', 'backup', 'emergencia', 'cortes', 'autonomia']
    },
    'bombeo': {
        'nombre': 'Bombeo Solar Fotovoltaico',
        'descripcion': 'Sistemas de bombeo solar sin diésel ni costos eléctricos. Bombeo desde profundidades de hasta 100m con paneles de alta eficiencia y variadores inteligentes. Ideal para riego agrícola, ganadería y comunidades.',
        'keywords': ['bombeo', 'riego', 'agua', 'agricultura', 'pozo', 'ganaderia', 'comunidad']
    },
    'iluminacion': {
        'nombre': 'Iluminación LED Solar',
        'descripcion': 'Soluciones de iluminación solar autónoma con tecnología LED de última generación. Ideal para espacios públicos, calles, parques y seguridad. Sensores de presencia y control inteligente.',
        'keywords': ['iluminacion', 'luz', 'led', 'calle', 'parque', 'emergencia', 'seguridad']
    },
    'eficiencia': {
        'nombre': 'Eficiencia Energética',
        'descripcion': 'Auditorías energéticas integrales y diagnóstico profesional. Automatización de procesos con control inteligente para reducir costos operativos y mejorar productividad. Análisis de consumo y optimización.',
        'keywords': ['eficiencia', 'optimizar', 'consumo', 'auditoria', 'reducir', 'diagnostico']
    },
    'industria': {
        'nombre': 'Industria 4.0 e IoT',
        'descripcion': 'Plataformas de monitoreo y control remoto del consumo eléctrico. Supervisión en línea con alertas automáticas, reportes en tiempo real e integración con dispositivos industriales y domésticos. Digitalización de procesos.',
        'keywords': ['industria', 'automatizacion', 'iot', 'procesos', '4.0', 'monitoreo', 'control', 'remoto', 'plataforma']
    }
}

# Mapeo de intenciones a palabras clave
INTENT_KEYWORDS = {
    'saludo': ['hola', 'buenos', 'buenas', 'saludos', 'hey', 'hi'],
    'consulta_servicios': ['servicio', 'ofrecen', 'tienen', 'hacen', 'producto', 'productos'],
    'info_general': ['informacion', 'info', 'sobre', 'acerca', 'que es', 'quienes son', 'empresa'],
    'precio': ['precio', 'costo', 'cotizacion', 'cuanto', 'valor', 'presupuesto'],
    'contacto': ['contacto', 'llamar', 'telefono', 'whatsapp', 'escribir', 'comunicar', 'hablar'],
    'confirmacion_si': ['si', 'sí', 'claro', 'ok', 'dale', 'quiero', 'deseo', 'me interesa', 'afirmativo', 'perfecto', 'acepto'],
    'confirmacion_no': ['no', 'nada', 'negativo', 'luego', 'despues', 'mas tarde'],
    'instalacion': ['instalar', 'instalacion', 'montar', 'montaje', 'como funciona', 'proceso'],
    'tiempo': ['tiempo', 'plazo', 'duracion', 'cuanto tarda', 'demora', 'cuando'],
    'ubicacion': ['donde', 'ubicacion', 'atienden', 'zona', 'area', 'trabajan'],
    'garantia': ['garantia', 'garantía', 'respaldo', 'mantenimiento']
}

# Ejemplos de proyectos reales por servicio
PROYECTOS_EJEMPLO = {
    'solar_aislada': [
        'Sistema Off-Grid 5 kWh con paneles bifaciales en El Carmen (Manabí)',
        'Sistema de seguridad solar en Liguiqui (cámaras, portero, apertura motorizada)',
        'Sistemas residenciales de 3 kW con autonomía completa'
    ],
    'solar_red': [
        'Solar On-Grid 9 kW - Lavadora y Lubricadora J (Manta)',
        'Infraestructura fotovoltaica EPAM (Empresa Pública Aguas Manta)',
        'Múltiples instalaciones comerciales en Manabí'
    ],
    'solar_hibrido': [
        'Sistema híbrido 5 kW con baterías de litio 10 kWh',
        'Sistema solar-eólico 7 kW con autonomía de 2 días',
        'Soluciones de respaldo para comercios y oficinas'
    ],
    'bombeo': [
        'Bombeo Solar 6.5 kW en Comuna Liguiqui',
        '18 paneles solares de alta eficiencia',
        'Bombeo desde 60m de profundidad',
        'Abastecimiento hasta 700m de distancia',
        'Elevación de 120m sin diésel ni costos eléctricos'
    ],
    'iluminacion': [
        'Iluminación solar en espacios públicos',
        'Sistemas de seguridad con sensores de presencia',
        'Alumbrado para comunidades rurales sin red eléctrica'
    ],
    'eficiencia': [
        'Auditorías energéticas para empresas industriales',
        'Optimización de consumo en edificios comerciales',
        'Automatización inteligente de procesos'
    ],
    'industria': [
        'Plataformas de monitoreo remoto 24/7',
        'Control inteligente de consumo eléctrico',
        'Integración IoT en procesos industriales',
        'Alianzas con Growatt, Siemens y Tier 1'
    ]
}

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def detectar_intencion(mensaje):
    """
    Detecta la intención del usuario basándose en palabras clave
    
    Args:
        mensaje (str): Mensaje del usuario
        
    Returns:
        str: Intención detectada
    """
    mensaje_lower = mensaje.lower()
    
    # Verificar intenciones generales
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in mensaje_lower for keyword in keywords):
            return intent
    
    # Detectar servicio específico
    for servicio_key, servicio in SERVICIOS.items():
        if any(keyword in mensaje_lower for keyword in servicio['keywords']):
            return f'servicio_{servicio_key}'
    
    return 'general'


def obtener_sesion(session_id):
    """
    Obtiene o crea una sesión de usuario
    
    Args:
        session_id (str): ID de la sesión
        
    Returns:
        dict: Datos de la sesión
    """
    if session_id not in sessions:
        sessions[session_id] = {
            'estado': 'inicial',
            'servicio_interes': None,
            'mensajes': [],
            'datos_usuario': {}
        }
    return sessions[session_id]


def generar_url_whatsapp(servicio_nombre, contexto_adicional=''):
    """
    Genera URL de WhatsApp con mensaje pre-formateado
    
    Args:
        servicio_nombre (str): Nombre del servicio de interés
        contexto_adicional (str): Contexto adicional opcional
        
    Returns:
        str: URL de WhatsApp formateada
    """
    if contexto_adicional:
        mensaje = f"Hola, requiero información sobre {servicio_nombre}. {contexto_adicional}"
    else:
        mensaje = f"Hola, requiero información sobre {servicio_nombre}"
    
    # Codificar el mensaje para URL
    mensaje_codificado = mensaje.replace(' ', '%20').replace(',', '%2C').replace('\n', '%0A')
    
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={mensaje_codificado}"


def extraer_contexto_conversacion(mensajes, limite=5):
    """
    Extrae contexto relevante de mensajes anteriores
    
    Args:
        mensajes (list): Lista de mensajes de la sesión
        limite (int): Número máximo de mensajes a revisar
        
    Returns:
        str: Contexto extraído o cadena vacía
    """
    for msg in mensajes[-limite:]:
        if msg['tipo'] == 'usuario' and len(msg['texto']) > 20:
            return f"Información adicional: {msg['texto'][:100]}"
    return ''


def formatear_proyectos(proyectos):
    """
    Formatea lista de proyectos para mostrar
    
    Args:
        proyectos (list): Lista de proyectos
        
    Returns:
        str: Proyectos formateados
    """
    return '\n'.join([f"• {proyecto}" for proyecto in proyectos])


# ============================================================================
# GENERADORES DE RESPUESTAS
# ============================================================================

def respuesta_saludo():
    """Genera respuesta de saludo inicial"""
    return """¡Hola! Bienvenido a Sparks IoT & Energy

Somos una empresa de ingeniería especializada en soluciones tecnológicas para energía, automatización e Industria 4.0.

Nuestra misión: Reducir costos, mejorar desempeño operativo y apoyar la transición hacia un futuro más limpio para empresas, instituciones y hogares en Ecuador.

¿En qué podemos ayudarte?
• Energías renovables (Solar, Híbridos, Bombeo)
• Eficiencia energética y automatización
• Industria 4.0 e IoT
• Proyectos de ingeniería eléctrica y electrónica"""


def respuesta_consulta_servicios():
    """Genera respuesta con listado de servicios"""
    return """Nuestros Servicios Especializados:

SOLAR OFF-GRID (AISLADA)
Sistemas autónomos con baterías de litio. Independencia total de la red eléctrica.

SOLAR ON-GRID (CONECTADA)
Reduce tu factura eléctrica inyectando excedentes. Balance cero con regulación ARCONEL.

SISTEMAS HÍBRIDOS
Lo mejor de ambos mundos: conectado a red + respaldo de baterías. Seguridad energética 24/7.

BOMBEO SOLAR
Bombeo desde profundidades de hasta 100m sin diésel. Ideal para agricultura y comunidades.

ILUMINACIÓN LED SOLAR
Soluciones autónomas con sensores inteligentes para espacios públicos y privados.

EFICIENCIA ENERGÉTICA
Auditorías integrales, diagnóstico y automatización para reducir costos operativos.

INDUSTRIA 4.0 E IOT
Monitoreo remoto, control inteligente, alertas automáticas y reportes en tiempo real.

¿Sobre cuál servicio te gustaría conocer más detalles?"""


def respuesta_servicio_detalle(servicio, proyectos):
    """
    Genera respuesta con detalles de un servicio específico
    
    Args:
        servicio (dict): Información del servicio
        proyectos (list): Lista de proyectos ejemplo
        
    Returns:
        str: Respuesta formateada
    """
    proyectos_texto = formatear_proyectos(proyectos) if proyectos else ''
    
    return f"""{servicio['nombre']}

{servicio['descripcion']}

PROYECTOS REALES:
{proyectos_texto}

NUESTRO PROCESO COMPLETO:
• Estudio energético integral (GRATUITO)
• Visita técnica y medición en sitio
• Análisis de patrones de consumo
• Proyección económica del ahorro y ROI
• Opciones de financiación y tramitación
• Instalación profesional certificada
• Monitoreo y seguimiento post-venta
• Garantías extendidas de equipos e instalación

BENEFICIOS:
• Ahorro inmediato en factura eléctrica
• Reducción de huella de carbono
• Independencia energética
• Aumento del valor de tu propiedad

¿Te gustaría que un asesor técnico especializado se comunique contigo para diseñar tu sistema ideal?"""


def respuesta_info_general():
    """Genera respuesta con información general de la empresa"""
    return f"""Sobre Sparks IoT & Energy

Somos una empresa de ingeniería especializada en soluciones tecnológicas para energía, automatización e Industria 4.0 en Ecuador.

NUESTRO ENFOQUE:
• Proyectos de ingeniería eléctrica, electrónica y automatización
• Orientados a eficiencia energética y digitalización industrial
• Generación renovable y reducción de huella de carbono

OBJETIVO:
Reducir costos operativos, mejorar desempeño y apoyar la transición hacia un futuro más limpio para empresas, instituciones y hogares.

PROYECTOS DESTACADOS:
• Sistema Off-Grid 5 kWh con paneles bifaciales (El Carmen, Manabí)
• Solar On-Grid 9 kW - Lavadora y Lubricadora J (Manta)
• Infraestructura fotovoltaica para EPAM (Empresa Pública de Aguas Manta)
• Bombeo Solar 6.5 kW desde 60m de profundidad (Comuna Liguiqui)
• Sistemas híbridos residenciales hasta 10 kWh de almacenamiento
• Automatización solar en Liguiqui (seguridad, cámaras, portero automático)

ALIANZAS TECNOLÓGICAS:
Trabajamos con marcas líderes como Growatt, Siemens y fabricantes Tier 1 para garantizar sistemas duraderos e inteligentes.

UBICACIÓN:
{COMPANY_INFO['address']}
{COMPANY_INFO['city']}

CONTACTO:
• Teléfonos: {' / '.join(COMPANY_INFO['phones'])}
• WhatsApp: {COMPANY_INFO['whatsapp']}
• Email: {COMPANY_INFO['email']}
• Web: {COMPANY_INFO['website']}

¿Te gustaría conocer nuestros servicios específicos o ver más proyectos?"""


def respuesta_precio():
    """Genera respuesta sobre precios y cotizaciones"""
    return """Cotización y Presupuestos

Los costos de un sistema solar varían según múltiples factores:

VARIABLES QUE DETERMINAN EL PRECIO:
• Tipo de instalación: On-Grid, Off-Grid o Híbrido
• Capacidad del sistema: kW necesarios según tu consumo
• Almacenamiento: Con o sin baterías (litio vs plomo)
• Ubicación: Accesibilidad, tipo de tejado, distancia
• Componentes: Marcas premium vs estándar
• Complejidad: Instalación residencial vs industrial

RANGOS REFERENCIALES:
• Sistema residencial básico: Desde $2,500 USD
• Sistema comercial mediano: $8,000 - $20,000 USD
• Proyectos industriales: Cotización personalizada

LO QUE INCLUYE:
• Estudio energético integral (sin costo)
• Diseño personalizado del sistema
• Todos los equipos y materiales
• Instalación profesional certificada
• Tramitación de permisos
• Capacitación y puesta en marcha
• Garantías extendidas

RETORNO DE INVERSIÓN:
La mayoría de sistemas se pagan solos en 4-7 años con el ahorro en factura eléctrica.

Para una cotización precisa y personalizada, ofrecemos un estudio técnico gratuito donde evaluamos tu consumo actual y diseñamos el sistema ideal.

¿Te gustaría agendar tu asesoría técnica sin costo? Puedo conectarte por WhatsApp."""


def respuesta_instalacion():
    """Genera respuesta sobre proceso de instalación"""
    return """Proceso de Instalación - ¿Cómo funciona?

La instalación de un sistema solar es el proceso de montar y conectar todos los componentes necesarios para generar energía limpia. Esto incluye paneles solares, inversores, estructuras de montaje, cableado y sistemas de protección.

NUESTRO PROCESO PROFESIONAL:

1. VISITA TÉCNICA GRATUITA
   - Evaluamos tu tejado/terreno, orientación solar
   - Medimos tu consumo eléctrico actual
   - Analizamos la radiación solar de tu zona

2. PROPUESTA PERSONALIZADA
   - Diseñamos el sistema ideal para tus necesidades
   - Cotización detallada con ROI y ahorro mensual
   - Simulación de producción energética

3. INSTALACIÓN PROFESIONAL
   - Montaje de estructura y paneles
   - Instalación de inversor y protecciones
   - Conexión al sistema eléctrico
   - Duración: 2-5 días según tamaño

4. PUESTA EN MARCHA
   - Pruebas de funcionamiento
   - Capacitación de uso y monitoreo
   - Entrega de documentación técnica

5. SEGUIMIENTO POST-VENTA
   - Monitoreo remoto del sistema
   - Soporte técnico continuo
   - Mantenimientos preventivos

¿Te gustaría que un técnico visite tu ubicación para evaluar tu caso? Puedo conectarte por WhatsApp."""


def respuesta_tiempo():
    """Genera respuesta sobre tiempos de implementación"""
    return """Tiempos de Implementación - Planifica tu proyecto

Cada proyecto solar tiene diferentes fases que requieren tiempo específico. Es importante conocer estos plazos para planificar tu inversión.

CRONOGRAMA TÍPICO:

EVALUACIÓN INICIAL: 24-48 horas
→ Visita técnica para análisis del sitio
→ Qué hacemos: medición de espacio, consumo, viabilidad

DISEÑO Y PROPUESTA: 3-5 días hábiles
→ Ingeniería del sistema personalizado
→ Qué incluye: planos, equipos, presupuesto, simulación

INSTALACIÓN FÍSICA:
• Residencial (2-5 kW): 2-3 días
  Ideal para casas, pequeños negocios

• Comercial (5-20 kW): 5-7 días
  Para oficinas, talleres, comercios medianos

• Industrial (20+ kW): 2-3 semanas
  Grandes instalaciones, naves industriales

TRÁMITES Y PERMISOS: 2-4 semanas
Solo para sistemas conectados a la red eléctrica
→ Permisos municipales
→ Homologación con empresa eléctrica
→ Inspecciones y aprobaciones

POR QUÉ VARÍA EL TIEMPO:
• Tamaño y complejidad del sistema
• Tipo de estructura (tejado, suelo, industrial)
• Disponibilidad de equipos importados
• Clima y temporada
• Permisos gubernamentales

TIP: La mayoría de proyectos residenciales están operativos en 3-4 semanas desde el primer contacto.

¿Deseas iniciar el proceso? Puedo conectarte con un asesor por WhatsApp para coordinar tu visita."""


def respuesta_ubicacion():
    """Genera respuesta sobre ubicación y cobertura"""
    return f"""Ubicación y Zona de Cobertura

La ubicación geográfica es crucial en proyectos solares porque determina:

RADIACIÓN SOLAR DISPONIBLE
Ecuador tiene excelente radiación, pero varía por región
La costa tiene aproximadamente 4.5-5.5 kWh/m²/día (muy bueno para solar)

LOGÍSTICA Y SOPORTE
Cercanía con nuestros técnicos reduce tiempos y costos
Garantiza respuesta rápida ante cualquier eventualidad

NORMATIVAS LOCALES
Cada municipio tiene regulaciones específicas
Conocemos los procesos y requisitos en nuestra zona

NUESTRA OFICINA PRINCIPAL:
{COMPANY_INFO['address']}
{COMPANY_INFO['city']}

ZONAS DE ATENCIÓN:

COBERTURA TOTAL (servicio completo):
• Manta - Base de operaciones
• Portoviejo
• Montecristi
• Jaramijó
• Crucita, San Mateo, San Jacinto
• El Carmen
• Liguiqui
• Toda la provincia de Manabí

PROYECTOS ESPECIALES:
• Otras provincias de Ecuador
• Sistemas industriales (+50 kW)
• Instalaciones comerciales grandes

CANALES DE CONTACTO:
• WhatsApp: {COMPANY_INFO['whatsapp']}
• Teléfonos: {' / '.join(COMPANY_INFO['phones'])}
• Email: {COMPANY_INFO['email']}
• Web: {COMPANY_INFO['website']}

NOTA: Evaluamos proyectos en todo Ecuador. Instalaciones industriales y comerciales grandes justifican movilización nacional.

¿Tu proyecto está en nuestra zona? Cuéntame tu ubicación y te confirmo. También puedo conectarte directamente por WhatsApp."""


def respuesta_garantia():
    """Genera respuesta sobre garantías"""
    return """Garantías y Respaldo - Tu inversión protegida

Una garantía es el compromiso del fabricante o instalador de reparar o reemplazar un producto si falla. En energía solar, las garantías son extensas porque los equipos están diseñados para durar décadas.

GARANTÍAS DE EQUIPOS:

PANELES SOLARES: 25 años
→ Qué cubre: Garantía de producción al 80% después de 25 años
→ Por qué es importante: Los paneles pierden aproximadamente 0.5% eficiencia/año
→ Qué significa: Generarán energía por 30-40 años
→ Marcas: Trabajamos con Tier 1 (JA Solar, Trina, Canadian Solar)

INVERSORES: 5-10 años
→ Qué es: Convierte corriente continua (DC) a alterna (AC)
→ Qué cubre: Defectos de fabricación, fallas electrónicas
→ Extensiones: Algunas marcas ofrecen hasta 20 años
→ Nota: Es el componente que puede requerir reemplazo

BATERÍAS: 5-10 años o ciclos
→ Qué es: Almacena energía para uso nocturno
→ Qué cubre: Capacidad mínima garantizada por ciclos
→ Tipos: Litio (10 años/6000 ciclos) vs Plomo (5 años/1500 ciclos)

ESTRUCTURA DE MONTAJE: 10 años
→ Qué cubre: Corrosión, deformaciones, desprendimientos
→ Material: Aluminio o acero galvanizado

GARANTÍA DE INSTALACIÓN:

MANO DE OBRA: 2 años (Sparks IoT & Energy)
→ Qué cubre: Filtraciones, conexiones, cableado
→ Incluye: Revisiones sin costo ante cualquier problema
→ Instaladores: Técnicos certificados con experiencia

SOPORTE TÉCNICO: Incluido de por vida
→ Asesoría telefónica/WhatsApp
→ Diagnóstico remoto de fallas
→ Actualización de software de inversores

MANTENIMIENTO PREVENTIVO:

¿Qué es? Revisiones periódicas para optimizar rendimiento

INCLUYE:
• Limpieza de paneles (2 veces/año recomendado)
• Inspección de conexiones eléctricas
• Verificación de tensiones y corrientes
• Actualización de firmware
• Monitoreo remoto 24/7 de producción

PLANES DISPONIBLES:
• Plan Básico: 2 visitas/año
• Plan Premium: 4 visitas/año + monitoreo

CERTIFICACIONES INTERNACIONALES:
• IEC 61215 (paneles)
• IEC 61730 (seguridad)
• ISO 9001 (calidad)
• TUV, CE (certificaciones europeas)

¿Deseas más detalles sobre algún componente específico o las condiciones de garantía? Puedo conectarte con un asesor técnico por WhatsApp."""


def respuesta_confirmacion_whatsapp(servicio_nombre, numero_formateado):
    """
    Genera respuesta de confirmación para redirigir a WhatsApp
    
    Args:
        servicio_nombre (str): Nombre del servicio
        numero_formateado (str): Número de WhatsApp formateado
        
    Returns:
        str: Respuesta formateada
    """
    return f"""¡Perfecto!

Para brindarte la mejor atención personalizada, te conectaré directamente con nuestro equipo de especialistas por WhatsApp.

TU MENSAJE SERÁ:
"Hola, requiero información sobre {servicio_nombre}"

Al hacer clic en el botón verde de WhatsApp, se abrirá automáticamente la conversación con nuestro número {numero_formateado}.

Uno de nuestros asesores te responderá a la brevedad.

¿Deseas continuar por WhatsApp?"""


# ============================================================================
# ENDPOINTS DE LA API
# ============================================================================

@api_bp.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint principal para conversación con el chatbot
    
    Request JSON:
        message (str): Mensaje del usuario
        session_id (str): ID de sesión (opcional)
        
    Returns:
        JSON: Respuesta del chatbot con estado de sesión
    """
    try:
        data = request.get_json()
        
        # Validar entrada
        if not data or 'message' not in data:
            return jsonify({'error': 'Se requiere un mensaje'}), 400
        
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default-session')
        
        logger.info(f'Mensaje recibido: {user_message[:50]}... | Session: {session_id}')
        
        # Obtener sesión y agregar mensaje del usuario
        sesion = obtener_sesion(session_id)
        sesion['mensajes'].append({'tipo': 'usuario', 'texto': user_message})
        
        # Detectar intención del usuario
        intencion = detectar_intencion(user_message)
        logger.info(f'Intención detectada: {intencion}')
        
        # Variables para la respuesta
        response_text = ''
        whatsapp_url = None
        
        # ===== MANEJO DE INTENCIONES =====
        
        if intencion == 'saludo':
            response_text = respuesta_saludo()
            sesion['estado'] = 'presentacion'
        
        elif intencion == 'consulta_servicios':
            response_text = respuesta_consulta_servicios()
            sesion['estado'] = 'mostrando_servicios'
        
        elif intencion.startswith('servicio_'):
            servicio_key = intencion.replace('servicio_', '')
            if servicio_key in SERVICIOS:
                servicio = SERVICIOS[servicio_key]
                proyectos = PROYECTOS_EJEMPLO.get(servicio_key, [])
                
                response_text = respuesta_servicio_detalle(servicio, proyectos)
                sesion['servicio_interes'] = servicio_key
                sesion['estado'] = 'esperando_confirmacion'
        
        elif intencion == 'confirmacion_si' and sesion['estado'] == 'esperando_confirmacion':
            servicio_key = sesion.get('servicio_interes')
            if servicio_key and servicio_key in SERVICIOS:
                servicio = SERVICIOS[servicio_key]
                contexto = extraer_contexto_conversacion(sesion['mensajes'])
                whatsapp_url = generar_url_whatsapp(servicio['nombre'], contexto)
                response_text = respuesta_confirmacion_whatsapp(
                    servicio['nombre'],
                    COMPANY_INFO['whatsapp']
                )
                sesion['estado'] = 'redirigiendo_whatsapp'
            else:
                response_text = "Por favor, dime sobre qué servicio te gustaría recibir información."
        
        elif intencion == 'confirmacion_no' and sesion['estado'] == 'esperando_confirmacion':
            response_text = "No hay problema. ¿Hay algún otro servicio sobre el que quieras conocer más? O si prefieres, puedo contarte sobre cómo funcionamos."
            sesion['estado'] = 'mostrando_servicios'
        
        elif intencion == 'info_general':
            response_text = respuesta_info_general()
            sesion['estado'] = 'presentacion'
        
        elif intencion == 'precio':
            response_text = respuesta_precio()
            sesion['estado'] = 'ofreciendo_asesoria'
        
        elif intencion == 'contacto':
            response_text = """Contáctanos por WhatsApp

Puedo conectarte directamente con nuestro equipo técnico.

Dime qué servicio te interesa y te redirigiré inmediatamente a WhatsApp para que un especialista te atienda:

• Instalaciones Solares
• Sistemas de Bombeo
• Iluminación Solar
• Eficiencia Energética
• Industria 4.0

¿Cuál te interesa?"""
            sesion['estado'] = 'esperando_servicio_contacto'
        
        elif intencion == 'instalacion':
            response_text = respuesta_instalacion()
            sesion['estado'] = 'ofreciendo_visita'
        
        elif intencion == 'tiempo':
            response_text = respuesta_tiempo()
            sesion['estado'] = 'ofreciendo_visita'
        
        elif intencion == 'ubicacion':
            response_text = respuesta_ubicacion()
            sesion['estado'] = 'consultando_ubicacion'
        
        elif intencion == 'garantia':
            response_text = respuesta_garantia()
            sesion['estado'] = 'ofreciendo_asesoria'
        
        # ===== MANEJO DE ESTADOS ESPECIALES =====
        
        elif sesion['estado'] == 'esperando_servicio_contacto':
            mensaje_lower = user_message.lower()
            servicio_encontrado = None
            
            for key, servicio in SERVICIOS.items():
                if any(keyword in mensaje_lower for keyword in servicio['keywords']):
                    servicio_encontrado = servicio
                    sesion['servicio_interes'] = key
                    break
            
            if servicio_encontrado:
                whatsapp_url = generar_url_whatsapp(servicio_encontrado['nombre'])
                response_text = f"""¡Perfecto!

Te conectaré directamente con un especialista en {servicio_encontrado['nombre']} por WhatsApp.

Al hacer clic en el botón verde, se abrirá WhatsApp con tu mensaje prellenado:
"Hola, requiero información sobre {servicio_encontrado['nombre']}"

Nuestro equipo te responderá inmediatamente."""
                sesion['estado'] = 'redirigiendo_whatsapp'
            else:
                response_text = """No estoy seguro de haber entendido el servicio.

Por favor, elige uno de estos:
• Solar aislada o Solar red
• Bombeo solar
• Iluminación
• Eficiencia energética
• Industria 4.0"""
        
        elif sesion['estado'] == 'ofreciendo_visita':
            if any(word in user_message.lower() for word in ['si', 'claro', 'ok', 'dale']):
                servicio_interes = sesion.get('servicio_interes', 'Consulta general')
                servicio_nombre = SERVICIOS.get(servicio_interes, {}).get('nombre', servicio_interes)
                
                whatsapp_url = generar_url_whatsapp(
                    servicio_nombre,
                    "Solicito agendar una visita técnica."
                )
                response_text = """¡Excelente!

Te conectaré con nuestro equipo técnico por WhatsApp para coordinar tu visita.

Ellos se pondrán en contacto contigo en las próximas horas para:
• Confirmar tu ubicación
• Acordar fecha y hora
• Preparar el estudio preliminar

Haz clic en el botón verde de WhatsApp."""
                sesion['estado'] = 'redirigiendo_whatsapp'
            else:
                response_text = """No hay problema. ¿Hay algo más en lo que pueda ayudarte?

Puedo contarte sobre:
• Otros servicios
• Tiempos de instalación
• Garantías
• Financiamiento"""
                sesion['estado'] = 'conversacion'
        
        elif sesion['estado'] == 'ofreciendo_asesoria':
            if any(word in user_message.lower() for word in ['si', 'claro', 'ok', 'dale', 'whatsapp']):
                servicio_interes = sesion.get('servicio_interes', 'Asesoría técnica')
                servicio_nombre = SERVICIOS.get(servicio_interes, {}).get('nombre', servicio_interes)
                
                whatsapp_url = generar_url_whatsapp(servicio_nombre, "Solicito asesoría técnica detallada.")
                response_text = """¡Perfecto!

Te conectaré con un asesor técnico especializado por WhatsApp.

Nuestro equipo revisará tu caso y te ofrecerá:
• Asesoría técnica personalizada
• Cotización detallada
• Análisis de ahorro energético
• Recomendaciones específicas

Haz clic en el botón verde de WhatsApp para iniciar la conversación."""
                sesion['estado'] = 'redirigiendo_whatsapp'
            else:
                response_text = """Entendido. ¿Te gustaría saber más sobre algún otro tema?

• Proceso de instalación
• Garantías
• Zonas de cobertura
• Otros servicios"""
                sesion['estado'] = 'conversacion'
        
        elif sesion['estado'] == 'consultando_ubicacion':
            ubicacion_mencionada = user_message
            sesion['datos_usuario']['ubicacion'] = ubicacion_mencionada
            
            whatsapp_url = generar_url_whatsapp(
                "Consulta sobre cobertura",
                f"Mi ubicación es: {ubicacion_mencionada}. ¿Pueden atenderme?"
            )
            response_text = f"""Gracias por compartir tu ubicación: {ubicacion_mencionada}

Te conectaré con nuestro equipo comercial por WhatsApp para:
• Confirmar cobertura en tu zona
• Coordinar visita técnica
• Brindarte información específica de tu región

Haz clic en el botón verde de WhatsApp."""
            sesion['estado'] = 'redirigiendo_whatsapp'
        
        else:
            # Respuesta general para intenciones no manejadas
            response_text = """Estoy aquí para ayudarte con información sobre nuestros servicios de energías renovables.

Puedo contarte sobre:
• Instalaciones solares
• Sistemas de bombeo
• Iluminación solar
• Eficiencia energética
• Automatización industrial

¿Qué te interesa saber?"""
        
        # Guardar respuesta del bot en la sesión
        sesion['mensajes'].append({'tipo': 'bot', 'texto': response_text})
        
        # Preparar respuesta JSON
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
        logger.error(f'Error en /chat: {str(e)}', exc_info=True)
        return jsonify({'error': 'Error interno del servidor'}), 500


@api_bp.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """
    Obtiene información de una sesión específica
    
    Args:
        session_id (str): ID de la sesión
        
    Returns:
        JSON: Datos de la sesión o error 404
    """
    if session_id in sessions:
        return jsonify(sessions[session_id]), 200
    return jsonify({'error': 'Sesión no encontrada'}), 404


@api_bp.route('/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """
    Elimina una sesión específica
    
    Args:
        session_id (str): ID de la sesión
        
    Returns:
        JSON: Mensaje de confirmación
    """
    if session_id in sessions:
        del sessions[session_id]
        return jsonify({'message': 'Sesión eliminada'}), 200
    return jsonify({'error': 'Sesión no encontrada'}), 404


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de health check para monitoreo
    
    Returns:
        JSON: Estado del servicio
    """
    return jsonify({
        'status': 'healthy',
        'service': COMPANY_NAME,
        'timestamp': datetime.now().isoformat(),
        'active_sessions': len(sessions)
    }), 200
