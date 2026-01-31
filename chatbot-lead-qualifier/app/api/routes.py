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
        'keywords': ['aislada', 'off-grid', 'sin red', 'autonoma', 'bateria', 'rural', 'remota', 'hibrida']
    },
    'solar_red': {
        'nombre': 'Solar Fotovoltaica Conectada a Red (On-Grid)',
        'descripcion': 'Sistema conectado a red que permite generar tu propia energía e inyectar excedentes. Reduce tu factura eléctrica hasta alcanzar balance cero.',
        'keywords': ['conectada', 'on-grid', 'red', 'factura', 'ahorro', 'excedente', 'instalacion solar', 'instalaciones solares', 'energia solar', 'paneles solares', 'sistema solar']
    },
    'bombeo': {
        'nombre': 'Sistemas de Bombeo Solar',
        'descripcion': 'Bombeo o riego fotovoltaico que reduce costos de electricidad. Optimizado con variadores de frecuencia para máximo rendimiento.',
        'keywords': ['bombeo', 'riego', 'agua', 'agricultura', 'pozo', 'sistema de bombeo', 'sistemas de bombeo']
    },
    'iluminacion': {
        'nombre': 'Sistemas de Iluminación Solar',
        'descripcion': 'Iluminación LED solar para espacios públicos y privados. Ideal para parques, calles, emergencias con sensores de presencia.',
        'keywords': ['iluminacion', 'luz', 'led', 'calle', 'parque', 'emergencia', 'iluminacion solar', 'luminarias']
    },
    'eficiencia': {
        'nombre': 'Eficiencia Energética',
        'descripcion': 'Optimización de tu consumo energético mediante auditorías y soluciones personalizadas para reducir costos.',
        'keywords': ['eficiencia', 'optimizar', 'consumo', 'auditoria', 'reducir', 'eficiencia energetica', 'ahorro energetico']
    },
    'industria': {
        'nombre': 'Industria 4.0',
        'descripcion': 'Automatización de procesos industriales con IoT y tecnologías inteligentes para mayor eficiencia.',
        'keywords': ['industria', 'automatizacion', 'iot', 'procesos', '4.0', 'automatizacion industrial', 'control industrial', 'scada', 'plc']
    }
}

def detectar_intencion(mensaje):
    """Detecta la intención del usuario"""
    mensaje_original = mensaje
    mensaje = mensaje.lower().strip()
    
    # Manejar respuestas muy cortas o números (fuera de contexto)
    if len(mensaje) <= 2 and (mensaje.isdigit() or mensaje in ['ok', 'ya', 'ah']):
        return 'respuesta_confusa'
    
    # Saludos
    if any(word in mensaje for word in ['hola', 'buenos', 'buenas', 'saludos', 'hey', 'hi', 'buenos dias', 'buenas tardes']):
        return 'saludo'
    
    # Detectar servicio específico (PRIMERO para tener prioridad)
    for servicio_key, servicio in SERVICIOS.items():
        if any(keyword in mensaje for keyword in servicio['keywords']):
            return f'servicio_{servicio_key}'
    
    # Información sobre proyectos/experiencia
    if any(word in mensaje for word in ['proyecto', 'experiencia', 'casos', 'referencias', 'ejemplo', 'hicieron', 'realizaron', 'cartera']):
        return 'consulta_proyectos'
    
    # Certificaciones/ISO
    if any(word in mensaje for word in ['certificacion', 'iso', 'norma', 'estandar']):
        return 'consulta_certificaciones'
    
    # Información sobre marcas/equipos
    if any(word in mensaje for word in ['marca', 'inversor', 'equipo', 'panel', 'bateria', 'tecnologia', 'especif']):
        return 'consulta_marcas'
    
    # Contacto directo con asesor (ANTES de caso_real para priorizar contacto directo)
    if any(phrase in mensaje for phrase in ['hablar con asesor', 'quiero asesor', 'necesito asesor', 'contactar asesor', 'hablar con', 'comunicar con', 'llamar', 'telefono', 'whatsapp', 'contacto', 'escribir', 'contactarme', 'comunicar']):
        return 'contacto'
    
    # Caso real / Cotización personalizada
    if any(word in mensaje for word in ['caso real', 'mi caso', 'cotizar', 'cotizacion', 'evaluar mi caso', 'mi proyecto', 'asesorarme sobre mi proyecto']):
        return 'caso_real'
    
    # Procesos / Cómo funciona
    if any(word in mensaje for word in ['proceso', 'como funciona', 'como se hace', 'pasos', 'etapas', 'instalacion', 'implementacion', 'como realizan']):
        return 'consulta_procesos'
    
    # Financiamiento / Opciones de pago
    if any(word in mensaje for word in ['financiacion', 'financiamiento', 'credito', 'pago', 'pagos', 'cuotas', 'plazo', 'opciones de financiacion', 'formas de pago', 'facilidades']):
        return 'consulta_financiamiento'
    
    # Precio/Cotización (ANTES que servicios para mayor especificidad)
    if any(word in mensaje for word in ['precio', 'costo', 'cuanto', 'valor', 'inversion', 'presupuesto']):
        return 'precio'
    
    # Energías Renovables en general
    if any(phrase in mensaje for phrase in ['energia renovable', 'energias renovables', 'energia limpia', 'energia verde', 'energia solar']):
        return 'consulta_energias_renovables'
    
    # Múltiples servicios mencionados
    servicios_mencionados = 0
    if any(word in mensaje for word in ['eficiencia energetica', 'eficiencia', 'optimizar']):
        servicios_mencionados += 1
    if any(word in mensaje for word in ['industria', '4.0', 'automatizacion', 'iot']):
        servicios_mencionados += 1
    if any(word in mensaje for word in ['solar', 'fotovoltaica', 'paneles']):
        servicios_mencionados += 1
    
    if servicios_mencionados >= 2:
        return 'consulta_multiples_servicios'
    
    # Redes sociales (ANTES de consulta_servicios para evitar conflictos)
    if any(word in mensaje for word in ['redes sociales', 'redes', 'instagram', 'facebook', 'tiktok', 'linkedin', 'youtube', 'twitter', 'siguenos', 'síguenos', 'síganos', 'red social', 'social media', '@sparks', 'seguir']):
        return 'redes_sociales'
    
    # Interés en servicios
    if any(word in mensaje for word in ['servicio', 'ofrecen', 'tienen', 'hacen', 'producto', 'ofrecer', 'servidos']):
        return 'consulta_servicios'
    
    # Información general
    if any(word in mensaje for word in ['informacion', 'info', 'sobre', 'acerca', 'que es', 'quienes son', 'empresa', 'hablame']):
        return 'info_general'
    
    # NEGACIONES Y CIERRES (MUY IMPORTANTE - revisar primero)
    # Negación fuerte con "no quiero"
    if any(phrase in mensaje for phrase in ['no quiero nada', 'no quiero', 'no me interesa', 'no gracias', 'no estoy interesado', 'por ahora no', 'no necesito', 'no deseo']):
        return 'cierre_conversacion'
    
    # Nada específico - cerrar
    if mensaje.strip() in ['nada', 'nada mas', 'nada más', 'ya nada', 'eso es todo', 'ya', 'solo eso']:
        return 'cierre_agradecimiento'
    
    # Confirmación positiva (DESPUÉS de verificar negaciones)
    if any(word in mensaje for word in ['si', 'sí', 'claro', 'ok', 'dale', 'quiero', 'deseo', 'me interesa', 'afirmativo', 'si please', 'aceptar', 'por favor', 'adelante']):
        # Verificar que no sea una negación disfrazada
        if 'no' not in mensaje:
            return 'confirmacion_si'
    
    # Negación simple
    if any(word in mensaje for word in ['no', 'negativo']) and len(mensaje.split()) <= 2:
        return 'confirmacion_no'
    
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

def generar_mensaje_whatsapp(sesion, servicio_nombre=''):
    """Genera el mensaje pre-formateado para WhatsApp con información del cliente"""
    # Número de WhatsApp de la empresa: +593 982840675
    numero = '593982840675'
    
    # Construir mensaje con información capturada
    usuario = sesion.get('usuario', 'Cliente')
    estado = sesion.get('estado', '')
    
    # Recopilar detalles de la conversación
    detalles = []
    if servicio_nombre:
        detalles.append(f"Servicio de interés: {servicio_nombre}")
    
    # Agregar contexto según el estado
    if 'caso_real' in sesion:
        detalles.append(f"Detalles del proyecto: {sesion['caso_real']}")
    
    # Construir el mensaje final
    mensaje_intro = f"Hola Sparks IoT&Energy, soy {usuario}"
    
    if detalles:
        mensaje_detalle = "%0A%0A".join(detalles)  # Saltos de línea en URL encoding
        mensaje_completo = f"{mensaje_intro}%0A%0A{mensaje_detalle}"
    else:
        mensaje_completo = f"{mensaje_intro} y deseo información sobre sus servicios de energía renovable"
    
    url_whatsapp = f"https://wa.me/{numero}?text={mensaje_completo}"
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
        
        # Capturar detalles del cliente si está en estado de solicitud de información
        if sesion.get('estado') == 'solicitando_caso_real' and len(user_message) > 20:
            # Guardar información proporcionada por el cliente
            if 'caso_real' not in sesion:
                sesion['caso_real'] = user_message
            else:
                sesion['caso_real'] += f" | {user_message}"
        
        # Detectar intención
        intencion = detectar_intencion(user_message)
        estado_actual = sesion.get('estado', 'inicial')
        logger.info(f'Intención detectada: {intencion} | Estado: {estado_actual}')
        
        response_text = ''
        whatsapp_url = None
        
        # Manejo de estados y respuestas
        # IMPORTANTE: Procesar servicios específicos ANTES de confirmaciones
        if intencion.startswith('servicio_'):
            servicio_key = intencion.replace('servicio_', '')
            if servicio_key in SERVICIOS:
                servicio = SERVICIOS[servicio_key]
                sesion['servicio_interes'] = servicio_key
                sesion['estado'] = 'esperando_confirmacion'
                
                # Respuestas detalladas por servicio
                detalles_servicios = {
                    'solar_aislada': """
**BENEFICIOS CLAVE:**
> 100% independencia de la red eléctrica
> Energía disponible 24/7 con almacenamiento
> Ideal para zonas rurales sin acceso a red
> Sistema robusto con baterías de litio o GEL
> Sin facturas eléctricas mensuales

**COMPONENTES:**
- Paneles solares monocristalinos
- Banco de baterias (Litio o GEL)
- Inversor Off-Grid
- Controlador de carga
- Estructura de montaje
- Sistema de proteccion

**APLICACIONES:**
- Viviendas rurales
- Fincas y haciendas
- Refugios de montana
- Estaciones remotas
- Videovigilancia aislada""",
                    'solar_red': """
**BENEFICIOS CLAVE:**
> Reduce tu factura hasta 90%
> Inyectas excedentes a la red
> Balance neto con la distribuidora
> Retorno de inversion: 3-5 anos
> Vida util: 25+ anos
> Incrementa el valor de tu propiedad

**COMPONENTES:**
- Paneles solares certificados
- Inversor On-Grid inteligente
- Medidor bidireccional
- Sistema de monitoreo en tiempo real
- Estructura de montaje
- Protecciones electricas

**IDEAL PARA:**
- Hogares con factura alta (>$80/mes)
- Negocios y comercios
- Oficinas
- Pequenas industrias
- Edificios""",
                    'bombeo': """
**BENEFICIOS CLAVE:**
> Elimina costos de diesel/electricidad
> Bombeo hasta 700m de distancia
> Optimizacion con variadores de frecuencia
> Sistema automatizado
> Bajo mantenimiento
> Operacion silenciosa

**COMPONENTES:**
- Paneles solares dimensionados
- Bomba sumergible o superficial
- Variador de frecuencia solar
- Controlador inteligente
- Sensores de nivel
- Tanque de almacenamiento (opcional)

**APLICACIONES:**
- Riego agricola
- Ganaderia
- Pozos profundos
- Reservorios
- Abastecimiento comunitario""",
                    'iluminacion': """
**BENEFICIOS CLAVE:**
> Cero costo de electricidad
> Instalacion rapida sin cableado
> Encendido/apagado automatico
> Sensores de movimiento
> Iluminacion LED de alta eficiencia
> Autonomia de 3-5 noches

**COMPONENTES:**
- Panel solar integrado
- Bateria de litio
- Luminaria LED (30-120W)
- Controlador inteligente
- Sensor crepuscular
- Sensor de movimiento (opcional)
- Poste y estructura

**APLICACIONES:**
- Alumbrado publico
- Parques y plazas
- Estacionamientos
- Caminos rurales
- Seguridad perimetral""",
                    'eficiencia': """
**BENEFICIOS CLAVE:**
> Reduccion de costos hasta 40%
> Optimizacion de recursos
> Identificacion de desperdicios
> Certificacion ISO 50001
> Mejora continua
> ROI en menos de 1 ano

**NUESTROS SERVICIOS:**
- Auditoria energetica completa
- Analisis de consumo por equipo
- Identificacion de oportunidades
- Plan de accion detallado
- Implementacion de mejoras
- Consultoria ISO 50001
- Monitoreo y seguimiento

**SECTORES:**
- Industrias
- Hoteles y restaurantes
- Hospitales
- Centros comerciales
- Oficinas corporativas""",
                    'industria': """
**BENEFICIOS CLAVE:**
> Automatizacion de procesos
> Reduccion de errores humanos
> Monitoreo en tiempo real
> Control remoto IoT
> Optimizacion de recursos
> Datos para toma de decisiones

**SOLUCIONES:**
- Sistemas PLC programables
- SCADA para supervision
- Variadores de frecuencia
- Control de motores
- Sensores IoT
- Estacion Sparks-AQ1 (calidad de aire)
- Integracion con sistemas existentes

**APLICACIONES:**
- Control de procesos
- Lineas de produccion
- Gestion energetica
- Calidad y trazabilidad
- Mantenimiento predictivo"""
                }
                
                detalle_extra = detalles_servicios.get(servicio_key, '')
                
                response_text = f"""**{servicio['nombre']}**

{servicio['descripcion']}
{detalle_extra}

**NUESTRO PROCESO:**
1. Estudio energético integral (SIN COSTO)
2. Visita técnica al sitio
3. Medición de patrones de consumo
4. Diseño personalizado
5. Proyección económica del ahorro
6. Opciones de financiación
7. Instalación profesional
8. Seguimiento y garantía

¿Te gustaría que un asesor técnico se comunique contigo para evaluar tu caso específico y brindarte una cotización personalizada?"""
        
        elif intencion == 'saludo':
            response_text = """Hola, bienvenido a Sparks IoT&Energy.

Somos una empresa ecuatoriana especializada en soluciones de energia renovable, eficiencia energetica e industria 4.0.

Puedo ayudarte con informacion sobre:
- Sistemas de energia solar (On-Grid, Off-Grid, Hibridos)
- Sistemas de bombeo solar
- Iluminacion LED solar
- Eficiencia energetica y auditorias
- Automatizacion industrial e IoT

Tambien puedo contarte sobre nuestros proyectos realizados, certificaciones o proceso de instalacion.

¿Que te gustaria saber?"""
            sesion['estado'] = 'inicio_conversacion'
        
        elif intencion == 'consulta_servicios':
            servicios_lista = []
            for key, srv in SERVICIOS.items():
                servicios_lista.append(f"- {srv['nombre']}")
            
            response_text = f"""**Nuestros Servicios Principales**

En Sparks IoT&Energy ofrecemos soluciones integrales en tres areas:

**ENERGIA SOLAR:**
- Sistema On-Grid (Conectado a red) - Reduce tu factura hasta 90%
- Sistema Off-Grid (Autonomo) - 100% independencia energetica
- Sistema Hibrido - Lo mejor de ambos mundos
- Bombeo Solar - Para agricultura y ganaderia
- Iluminacion LED Solar - Alumbrado publico y privado

**EFICIENCIA ENERGETICA:**
- Auditorias energeticas completas
- Consultoria ISO 50001
- Optimizacion de recursos
- Reduccion de costos operativos

**INDUSTRIA 4.0:**
- Automatizacion de procesos (PLC, SCADA)
- Sistemas IoT y monitoreo remoto
- Variadores de frecuencia
- Estacion Sparks-AQ1 (calidad de aire)

¿Te gustaria conocer mas detalles sobre alguno de estos servicios en particular?"""
            sesion['estado'] = 'mostrando_servicios'
        
        elif intencion == 'confirmacion_si' and sesion['estado'] in ['esperando_confirmacion', 'solicitando_caso_real', 'explicando_procesos', 'mostrando_servicios_completos', 'explicando_financiamiento', 'ofreciendo_asesoria', 'mostrando_contacto', 'mostrando_redes']:
            servicio_key = sesion.get('servicio_interes', 'consulta_general')
            if servicio_key and servicio_key in SERVICIOS:
                servicio = SERVICIOS[servicio_key]
                
                whatsapp_url = generar_mensaje_whatsapp(sesion, servicio['nombre'])
                
                response_text = f"""Perfecto, excelente decision.

Te conectare con uno de nuestros ingenieros especializados en {servicio['nombre']}.

El asesor podra:
- Responder todas tus preguntas especificas
- Evaluar tu caso en detalle
- Agendar una visita tecnica SIN COSTO
- Preparar una cotizacion personalizada

Te redirigire a WhatsApp donde nuestro equipo te atendera de inmediato.

Deseas abrir WhatsApp ahora?"""
                sesion['estado'] = 'redirigiendo_whatsapp'
            else:
                # Si no hay servicio específico, ofrecer contacto directo
                contacto = obtener_contacto_empresa()
                whatsapp_numeros = contacto.get('whatsapp', [])
                numero_whatsapp_principal = whatsapp_numeros[0].replace('+', '').replace(' ', '') if whatsapp_numeros else ''
                
                mensaje_whatsapp = "Hola Sparks IoT&Energy, me gustaria recibir asesoria tecnica personalizada"
                if numero_whatsapp_principal:
                    whatsapp_url = f"https://wa.me/{numero_whatsapp_principal}?text={mensaje_whatsapp.replace(' ', '%20')}"
                
                response_text = f"""Excelente.

Te conectaré directamente con nuestro equipo técnico por WhatsApp para una asesoría personalizada.

Nuestros ingenieros podrán:
- Evaluar tu caso específico
- Responder preguntas técnicas detalladas
- Agendar una visita sin costo
- Preparar una cotización personalizada

¿Deseas abrir WhatsApp ahora?"""
                sesion['estado'] = 'redirigiendo_whatsapp'
        
        elif intencion == 'confirmacion_no' and sesion['estado'] in ['esperando_confirmacion', 'explicando_financiamiento', 'ofreciendo_asesoria']:
            response_text = """Entendido, sin problema.

Gracias por tu tiempo. Si en el futuro necesitas asesoramiento sobre energia solar, eficiencia energetica o automatizacion industrial, aqui estamos para ayudarte.

Que tengas un excelente dia."""
            sesion['estado'] = 'conversacion_finalizada'
        
        elif intencion == 'info_general':
            empresa = obtener_informacion_empresa()
            response_text = f"""**Sobre {empresa.get('nombre_oficial', 'Sparks IoT&Energy')}**

{empresa.get('descripcion', 'Soluciones tecnológicas para ciudades inteligentes y sostenibles.')}

Ubicación: {empresa.get('ubicacion_principal', {}).get('nombre', '')}, Manta, Ecuador

**Nuestra Misión:**
{empresa.get('mision', '')}

**Nuestra Visión:**
{empresa.get('vision', '')}

**Nuestro Posicionamiento:**
Somos tu {empresa.get('posicionamiento', 'aliado estratégico')} en la transición energética.

¿Te gustaría conocer nuestros servicios específicos o proyectos de referencia?"""
            sesion['estado'] = 'presentacion'
        
        elif intencion == 'consulta_proyectos':
            proyectos = obtener_proyectos_referencia()
            response_text = """**Nuestros Proyectos de Referencia**

Contamos con una cartera de proyectos exitosos en tres sectores:

**RESIDENCIAL:**
• Urbanización Barú (Manta): Sistema On-Grid 5 kW
• Ciudad del Mar (Manta): Sistema On-Grid 10 kW + Sistema Híbrido 5 kW

**COMERCIAL:**
• Motel Intimus (Jipijapa): Sistema solar 22 kW (40 paneles)
• Multiservicios Julio (Manta): Sistema 15 kW

**PÚBLICO Y COMUNITARIO:**
• EPAM Manta: Infraestructura fotovoltaica en 8 puntos estratégicos
• Comuna Liguiqui: Sistema de Bombeo Solar (abastece a 700m) + Sistema Off-Grid para videovigilancia

Estos proyectos demuestran nuestra experiencia y confiabilidad. ¿Te gustaría saber más sobre alguno en particular?"""
            sesion['estado'] = 'mostrando_proyectos'
        
        elif intencion == 'consulta_certificaciones':
            response_text = """**Nuestras Certificaciones y Estándares**

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
            response_text = f"""**Marcas y Tecnología Utilizada**

Trabajamos con marcas líderes del mercado probadas en nuestros proyectos:
- JinkoSolar: Paneles de alta eficiencia
- SIEMENS: Sistemas de automatización
- INVT: Variadores de frecuencia
- GROOWATT: Inversores solares

**Tecnología:**
Paneles Monocristalinos para máxima eficiencia
Inversores On-Grid, Off-Grid e Híbridos
Almacenamiento: Baterías de Litio (larga duración) y GEL (aplicaciones rurales)
Sistemas PLC y SCADA para control industrial
IoT: Estación Sparks-AQ1 para monitoreo de aire y parámetros ambientales

Para detalles técnicos específicos de tu proyecto, consulta directamente con nuestros ingenieros vía WhatsApp.

¿Cuál servicio te interesa?"""
            sesion['estado'] = 'mostrando_servicios'
        
        elif intencion == 'precio':
            response_text = """**Sobre Precios y Cotización**

Los costos varían según:
• Tipo de instalación (On-Grid, Off-Grid, Híbrida)
• Capacidad requerida (kW)
• Características del sitio
• Componentes seleccionados (paneles, inversores, baterías)
• Ubicación geográfica

**Nuestro Proceso:**
1. Estudio energético integral (SIN COSTO)
2. Análisis de tu patrón de consumo
3. Proyección económica del ahorro
4. Cotización personalizada
5. Opciones de financiación

¿Te gustaría agendar una asesoría técnica gratuita?"""
            sesion['estado'] = 'ofreciendo_asesoria'
        
        elif intencion == 'consulta_financiamiento':
            response_text = """**Opciones de Financiamiento**

Entendemos que la inversión inicial es importante. Por eso ofrecemos varias alternativas de pago:

**OPCIONES DISPONIBLES:**

1. **Pago de Contado**
   - Descuento especial del 5-10%
   - Sin intereses
   - Beneficio inmediato

2. **Financiamiento Directo con Sparks**
   - Entrada inicial flexible (20-30%)
   - Plazos: 6, 12, 18 o 24 meses
   - Tasas competitivas
   - Aprobación rápida

3. **Financiamiento Bancario**
   - Convenios con bancos locales
   - Plazos extendidos hasta 5 años
   - Crédito verde con tasas preferenciales
   - Te asesoramos en el proceso

4. **Leasing Operativo** (Para empresas)
   - Deducible de impuestos
   - Sin afectar línea de crédito
   - Incluye mantenimiento

**CALCULO DE RETORNO:**
La inversión típicamente se recupera en 3-5 años con el ahorro en tu factura eléctrica. Desde el mes 1 comienzas a ahorrar.

**EJEMPLO PRÁCTICO:**
Sistema de 5kW:
- Inversión: $5,000 - $6,000
- Ahorro mensual: $80 - $120
- Financiamiento 12 meses: ~$450/mes
- Tu ahorro cubre gran parte de la cuota

¿Te gustaría que un asesor te prepare un plan de financiamiento personalizado según tu caso?"""
            sesion['estado'] = 'explicando_financiamiento'
        
        elif intencion == 'contacto':
            contacto = obtener_contacto_empresa()
            whatsapp_numeros = contacto.get('whatsapp', [])
            numero_whatsapp_principal = whatsapp_numeros[0].replace('+', '').replace(' ', '') if whatsapp_numeros else ''
            
            # Crear URL de WhatsApp directo
            mensaje_whatsapp = "Hola Sparks IoT&Energy, me gustaría recibir información sobre sus servicios"
            if numero_whatsapp_principal:
                whatsapp_url = f"https://wa.me/{numero_whatsapp_principal}?text={mensaje_whatsapp.replace(' ', '%20')}"
            
            response_text = f"""**Contacta con Nuestro Equipo Directamente**

**WhatsApp (Respuesta Inmediata):**
{' | '.join(whatsapp_numeros)}

Tenemos asesores disponibles para atenderte de inmediato por WhatsApp.

**Correo Electronico:**
{contacto.get('correo', 'info@sparksenergy.io')}

**Horario de Atencion:**
{contacto.get('horario', 'Lunes a Sabado, 08:00 AM - 08:00 PM')}

**Ubicacion:**
Edificio Manta Business Center, Torre B, Piso 3, Oficina 301
Av. Malecon (Frente al Mall del Pacifico), Manta, Manabi, Ecuador

Haz clic en el boton de WhatsApp para conectarte ahora con un asesor tecnico."""
            sesion['estado'] = 'mostrando_contacto'
        
        elif intencion == 'redes_sociales':
            contacto = obtener_contacto_empresa()
            redes = contacto.get('redes_sociales', {})
            
            response_text = f"""**Si, tenemos redes sociales!**

Siguenos para estar al dia con:
- Proyectos recientes de energia solar
- Tips de ahorro energetico
- Innovaciones en energia renovable
- Casos de exito
- Promociones especiales

**Facebook:**
{redes.get('facebook', '')}

**Instagram:**
{redes.get('instagram', '')}

**YouTube:**
{redes.get('youtube', '')}

**LinkedIn:**
{redes.get('linkedin', '')}

**Twitter/X:**
{redes.get('twitter', '')}

No te pierdas nuestro contenido exclusivo sobre energia renovable.

¿Te gustaria conectarte directamente con un asesor por WhatsApp para consultar sobre nuestros servicios?"""
            sesion['estado'] = 'mostrando_redes'
        
        elif intencion == 'consulta_energias_renovables':
            response_text = """**Energías Renovables - El Futuro Sostenible**

Las energías renovables son fuentes de energía limpia e inagotable que provienen de recursos naturales:

**Energía Solar Fotovoltaica**
Convierte la luz del sol en electricidad mediante paneles solares. Es la más popular y versátil.

**Ventajas Principales:**
- Reduce tu factura eléctrica hasta 90%
- Fuente de energía limpia y sostenible
- Contribuye a la reducción de CO₂
- Autonomía energética
- Retorno de inversión en 3-5 años
- Vida útil de 25+ años

**Nuestro Compromiso:**
En Sparks IoT&Energy trabajamos por un mejor futuro para nuestro planeta, implementando soluciones solares que han beneficiado a:
• Más de 50 familias en el sector residencial
• 15+ empresas comerciales
• Proyectos públicos y comunitarios en Manabí

**Nuestras Soluciones Solares:**
- Sistemas Aislados (Off-Grid): Para zonas sin red eléctrica
- Sistemas Conectados a Red (On-Grid): Reducen tu factura
- Sistemas Híbridos: Lo mejor de ambos mundos
- Bombeo Solar: Para agricultura y ganadería

¿Te gustaría conocer más sobre alguna solución específica?"""
            sesion['estado'] = 'explicando_renovables'
        
        elif intencion == 'consulta_multiples_servicios':
            response_text = """**Nuestras 3 Líneas de Negocio Principales**

**1. EFICIENCIA ENERGÉTICA**
• Auditorías energéticas completas
• Análisis de consumo y patrones
• Identificación de oportunidades de ahorro
• Implementación de ISO 50001
• Reducción de costos operativos hasta 40%

**2. ENERGÍAS RENOVABLES (Solar)**
• Sistemas On-Grid (conectados a red)
• Sistemas Off-Grid (autónomos con baterías)
• Sistemas Híbridos
• Bombeo solar para agricultura
• Iluminación LED solar

**3. INDUSTRIA 4.0 Y AUTOMATIZACIÓN**
• Control y automatización de procesos
• Sistemas PLC y SCADA
• Monitoreo en tiempo real con IoT
• Optimización de bombeo con variadores
• Estación Sparks-AQ1 (monitoreo ambiental)

**Solución Integral:**
Lo interesante es que podemos combinar estas tres áreas en un solo proyecto integrado. Por ejemplo:
- Auditoría energética + Sistema solar = Máximo ahorro
- Automatización industrial + Eficiencia = Optimización total
- Solar + IoT = Monitoreo inteligente en tiempo real

¿Te gustaría profundizar en alguna de estas áreas específicamente, o prefieres que un asesor técnico te contacte para diseñar una solución combinada para tu caso?"""
            sesion['estado'] = 'mostrando_servicios_completos'
        
        elif intencion == 'caso_real':
            response_text = """**Perfecto! Evaluemos Tu Caso Especifico**

Excelente decision. Para darte la mejor asesoria, nuestro ingeniero necesitara conocer:

**Informacion basica de tu proyecto:**
- Tipo: Residencial, Comercial o Industrial
- Ubicacion
- Tu necesidad principal (reducir factura, independencia energetica, etc.)
- Factura electrica promedio (si aplica)

**Lo que haremos por ti (SIN COSTO):**
1. Visita tecnica al sitio
2. Analisis detallado de consumo
3. Evaluacion de viabilidad
4. Diseño personalizado del sistema
5. Proyeccion de ahorro economico
6. Plan de financiamiento a tu medida

**Siguiente Paso:**
Conectate ahora con uno de nuestros ingenieros especializados via WhatsApp.

Proporcionale estos detalles de tu proyecto y el te preparara una propuesta personalizada en 24-48 horas.

Haz clic en el boton de WhatsApp para comenzar."""
            sesion['estado'] = 'solicitando_caso_real'
        
        elif intencion == 'consulta_procesos':
            response_text = """**Nuestro Proceso de Implementación Paso a Paso**

**FASE 1: Evaluación y Diseño (1-2 semanas)**
- Visita técnica sin costo a tu ubicación
- Levantamiento de información y mediciones
- Análisis de patrones de consumo
- Diseño técnico personalizado
- Simulación de rendimiento
- Cálculo de retorno de inversión (ROI)

**FASE 2: Propuesta y Aprobación (3-5 días)**
- Presentación de propuesta técnica-económica
- Explicación detallada del sistema
- Revisión de opciones de financiamiento
- Firma de contrato
- Cronograma de instalación

**FASE 3: Implementación (2-4 semanas)**
- Adquisición de equipos certificados
- Preparación del sitio
- Instalación de paneles/equipos
- Conexión eléctrica y configuración
- Pruebas de funcionamiento
- Capacitación al usuario

**FASE 4: Seguimiento y Mantenimiento**
- Monitoreo de rendimiento
- Mantenimiento preventivo
- Soporte técnico permanente
- Garantía de equipos (10-25 años)
- Garantía de instalación (5 años)

**Proyectos Exitosos:**
Hemos completado más de 60 proyectos siguiendo este proceso riguroso, desde viviendas residenciales hasta grandes instalaciones industriales.

**Tiempo Total Estimado:** 4-8 semanas desde la visita inicial hasta el sistema operativo.

¿Te gustaría que un asesor técnico se comunique contigo para evaluar tu proyecto específico y darte un cronograma personalizado?"""
            sesion['estado'] = 'explicando_procesos'
        
        elif intencion == 'cierre_conversacion':
            response_text = """Entiendo perfectamente.

Gracias por tu tiempo y por considerar a Sparks IoT&Energy. 

Recuerda que estamos aquí cuando lo necesites. Nuestras puertas están siempre abiertas para:
• Consultas futuras sobre energías renovables
• Asesoría técnica gratuita
• Información sobre nuevos proyectos

**Contacto Directo:**
WhatsApp: +593 982840675
Correo: info@sparksenergy.io

Seguimos trabajando por un futuro más sostenible en Ecuador.

Que tengas un excelente día."""
            sesion['estado'] = 'conversacion_cerrada'
        
        elif intencion == 'cierre_agradecimiento':
            response_text = """Perfecto.

Ha sido un placer atenderte. Gracias por tu interés en Sparks IoT&Energy.

Recuerda que trabajamos por un futuro más sostenible para Ecuador.

Si en algún momento necesitas:
- Asesoría técnica gratuita
- Cotización personalizada  
- Información sobre proyectos

**Contáctanos:**
WhatsApp: +593 99 831 4186
Correo: info@sparksenergy.io
Horario: Lunes a Sábado, 08:00 AM – 08:00 PM

Que tengas un excelente día.

Estaremos encantados de ayudarte cuando lo necesites."""
            sesion['estado'] = 'conversacion_finalizada'
        
        elif intencion == 'respuesta_confusa':
            estado_actual = sesion.get('estado', 'inicial')
            
            if estado_actual in ['esperando_confirmacion', 'solicitando_caso_real', 'explicando_procesos', 'ofreciendo_asesoria']:
                response_text = """No estoy seguro de entender tu respuesta.

Para ayudarte mejor, por favor responde:

**Sí** o **Quiero** - Si deseas que un asesor técnico te contacte
**No** - Si prefieres conocer otras opciones
**Nada** o **No me interesa** - Si deseas finalizar la conversación

¿Qué prefieres?"""
            else:
                response_text = """Disculpa, no entendí bien tu mensaje.

Puedo ayudarte con:

- Información sobre servicios (solar, bombeo, iluminación, eficiencia, industria)
- Proyectos de referencia
- Proceso de instalación
- Precios y cotizaciones
- Información de contacto
- Redes sociales

Por favor, cuéntame en qué puedo ayudarte."""
            
            sesion['estado'] = 'aclarando_duda'
        
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

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint para monitoreo y Docker"""
    try:
        return jsonify({
            'status': 'healthy',
            'service': 'chatbot-sparks-energy',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat(),
            'checks': {
                'knowledge_base': len(KNOWLEDGE_BASE) > 0,
                'sessions': len(sessions),
            }
        }), 200
    except Exception as e:
        logger.error(f'Error en health check: {str(e)}')
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

from datetime import datetime