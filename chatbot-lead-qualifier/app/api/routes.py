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

def detectar_intencion(mensaje):
    """Detecta la intención del usuario"""
    mensaje = mensaje.lower()
    
    # Saludos
    if any(word in mensaje for word in ['hola', 'buenos', 'buenas', 'saludos', 'hey', 'hi']):
        return 'saludo'
    
    # Interés en servicios
    if any(word in mensaje for word in ['servicio', 'ofrecen', 'tienen', 'hacen', 'producto', 'productos']):
        return 'consulta_servicios'
    
    # Información general
    if any(word in mensaje for word in ['informacion', 'info', 'sobre', 'acerca', 'que es', 'quienes son', 'empresa']):
        return 'info_general'
    
    # Precio/Cotización
    if any(word in mensaje for word in ['precio', 'costo', 'cotizacion', 'cuanto', 'valor', 'presupuesto']):
        return 'precio'
    
    # Contacto directo
    if any(word in mensaje for word in ['contacto', 'llamar', 'telefono', 'whatsapp', 'escribir', 'comunicar', 'hablar']):
        return 'contacto'
    
    # Confirmación positiva
    if any(word in mensaje for word in ['si', 'sí', 'claro', 'ok', 'dale', 'quiero', 'deseo', 'me interesa', 'afirmativo', 'perfecto', 'acepto']):
        return 'confirmacion_si'
    
    # Negación
    if any(word in mensaje for word in ['no', 'nada', 'negativo', 'luego', 'despues', 'mas tarde']):
        return 'confirmacion_no'
    
    # Consultas sobre instalación
    if any(word in mensaje for word in ['instalar', 'instalacion', 'montar', 'montaje', 'como funciona', 'proceso']):
        return 'instalacion'
    
    # Consultas sobre tiempo/plazo
    if any(word in mensaje for word in ['tiempo', 'plazo', 'duracion', 'cuanto tarda', 'demora', 'cuando']):
        return 'tiempo'
    
    # Consultas sobre ubicación/zona
    if any(word in mensaje for word in ['donde', 'ubicacion', 'atienden', 'zona', 'area', 'trabajan']):
        return 'ubicacion'
    
    # Consultas sobre garantía
    if any(word in mensaje for word in ['garantia', 'garantía', 'respaldo', 'mantenimiento']):
        return 'garantia'
    
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

def generar_mensaje_whatsapp(servicio_nombre, contexto_adicional=''):
    """Genera el mensaje pre-formateado para WhatsApp"""
    if contexto_adicional:
        mensaje = f"Hola, requiero información sobre {servicio_nombre}. {contexto_adicional}"
    else:
        mensaje = f"Hola, requiero información sobre {servicio_nombre}"
    
    # Número de WhatsApp de Sparks IoT&Energy
    numero_whatsapp = "593985937244"
    
    # Codificar el mensaje para URL
    mensaje_codificado = mensaje.replace(' ', '%20').replace(',', '%2C').replace('\n', '%0A')
    url_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensaje_codificado}"
    
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
            response_text = """¡Hola! 👋 Bienvenido a **Sparks IoT & Energy**

🔧 Somos una empresa de **ingeniería especializada** en soluciones tecnológicas para energía, automatización e Industria 4.0.

🎯 **Nuestra misión**: Reducir costos, mejorar desempeño operativo y apoyar la transición hacia un futuro más limpio para empresas, instituciones y hogares en Ecuador.

**¿En qué podemos ayudarte?**
• Energías renovables (Solar, Híbridos, Bombeo)
• Eficiencia energética y automatización
• Industria 4.0 e IoT
• Proyectos de ingeniería eléctrica y electrónica

¿Qué te interesa conocer?"""
            sesion['estado'] = 'presentacion'
        
        elif intencion == 'consulta_servicios':
            response_text = """💡 **Nuestros Servicios Especializados:**

☀️ **Solar Off-Grid (Aislada)**
Sistemas autónomos con baterías de litio. Independencia total de la red eléctrica.

⚡ **Solar On-Grid (Conectada)**
Reduce tu factura eléctrica inyectando excedentes. Balance cero con regulación ARCONEL.

🔋 **Sistemas Híbridos**
Lo mejor de ambos mundos: conectado a red + respaldo de baterías. Seguridad energética 24/7.

💧 **Bombeo Solar**
Bombeo desde profundidades de hasta 100m sin diésel. Ideal para agricultura y comunidades.

💡 **Iluminación LED Solar**
Soluciones autónomas con sensores inteligentes para espacios públicos y privados.

📊 **Eficiencia Energética**
Auditorías integrales, diagnóstico y automatización para reducir costos operativos.

🏭 **Industria 4.0 e IoT**
Monitoreo remoto, control inteligente, alertas automáticas y reportes en tiempo real.

¿Sobre cuál servicio te gustaría conocer más detalles?"""
            sesion['estado'] = 'mostrando_servicios'
        
        elif intencion.startswith('servicio_'):
            servicio_key = intencion.replace('servicio_', '')
            if servicio_key in SERVICIOS:
                servicio = SERVICIOS[servicio_key]
                sesion['servicio_interes'] = servicio_key
                sesion['estado'] = 'esperando_confirmacion'
                
                # Ejemplos de proyectos reales según servicio
                proyectos_ejemplo = {
                    'solar_aislada': """
**🏆 Proyectos Reales:**
• Sistema Off-Grid 5 kWh con paneles bifaciales en El Carmen (Manabí)
• Sistema de seguridad solar en Liguiqui (cámaras, portero, apertura motorizada)
• Sistemas residenciales de 3 kW con autonomía completa""",
                    'solar_red': """
**🏆 Proyectos Reales:**
• Solar On-Grid 9 kW - Lavadora y Lubricadora J (Manta)
• Infraestructura fotovoltaica EPAM (Empresa Pública Aguas Manta)
• Múltiples instalaciones comerciales en Manabí""",
                    'solar_hibrido': """
**🏆 Proyectos Reales:**
• Sistema híbrido 5 kW con baterías de litio 10 kWh
• Sistema solar-eólico 7 kW con autonomía de 2 días
• Soluciones de respaldo para comercios y oficinas""",
                    'bombeo': """
**🏆 Proyecto Destacado:**
• Bombeo Solar 6.5 kW en Comuna Liguiqui
  → 18 paneles solares de alta eficiencia
  → Bombeo desde 60m de profundidad
  → Abastecimiento hasta 700m de distancia
  → Elevación de 120m sin diésel ni costos eléctricos
  → Sistema funcionando 24/7 sin interrupciones""",
                    'iluminacion': """
**🏆 Aplicaciones Implementadas:**
• Iluminación solar en espacios públicos
• Sistemas de seguridad con sensores de presencia
• Alumbrado para comunidades rurales sin red eléctrica""",
                    'eficiencia': """
**🏆 Soluciones Implementadas:**
• Auditorías energéticas para empresas industriales
• Optimización de consumo en edificios comerciales
• Automatización inteligente de procesos""",
                    'industria': """
**🏆 Tecnologías Implementadas:**
• Plataformas de monitoreo remoto 24/7
• Control inteligente de consumo eléctrico
• Integración IoT en procesos industriales
• Alianzas con Growatt, Siemens y Tier 1"""
                }
                
                ejemplo = proyectos_ejemplo.get(servicio_key, '')
                
                response_text = f"""📌 **{servicio['nombre']}**

{servicio['descripcion']}
{ejemplo}

**✅ Nuestro Proceso Completo:**
• 🔍 Estudio energético integral (GRATUITO)
• 📐 Visita técnica y medición en sitio
• 📊 Análisis de patrones de consumo
• 💰 Proyección económica del ahorro y ROI
• 💳 Opciones de financiación y tramitación
• 🔧 Instalación profesional certificada
• 📡 Monitoreo y seguimiento post-venta
• 🛡️ Garantías extendidas de equipos e instalación

**🎯 Beneficios:**
✓ Ahorro inmediato en factura eléctrica
✓ Reducción de huella de carbono
✓ Independencia energética
✓ Aumento del valor de tu propiedad

¿Te gustaría que un asesor técnico especializado se comunique contigo para diseñar tu sistema ideal?"""
        
        elif intencion == 'confirmacion_si' and sesion['estado'] == 'esperando_confirmacion':
            servicio_key = sesion.get('servicio_interes')
            if servicio_key:
                servicio = SERVICIOS[servicio_key]
                
                # Capturar contexto adicional de mensajes anteriores
                contexto = ""
                for msg in sesion['mensajes'][-5:]:  # Últimos 5 mensajes
                    if msg['tipo'] == 'usuario' and len(msg['texto']) > 20:
                        contexto = f"Información adicional: {msg['texto'][:100]}"
                        break
                
                whatsapp_url = generar_mensaje_whatsapp(servicio['nombre'], contexto)
                
                response_text = f"""¡Perfecto! 🎉

Para brindarte la mejor atención personalizada, te conectaré directamente con nuestro equipo de especialistas por WhatsApp.

📱 **Tu mensaje será:**
"Hola, requiero información sobre {servicio['nombre']}"

Al hacer clic en el botón verde de WhatsApp, se abrirá automáticamente la conversación con nuestro número +593 98 593 7244.

Uno de nuestros asesores te responderá a la brevedad. 

¿Deseas continuar por WhatsApp?"""
                sesion['estado'] = 'redirigiendo_whatsapp'
            else:
                response_text = "Por favor, dime sobre qué servicio te gustaría recibir información."
        
        elif intencion == 'confirmacion_no' and sesion['estado'] == 'esperando_confirmacion':
            response_text = "No hay problema. ¿Hay algún otro servicio sobre el que quieras conocer más? O si prefieres, puedo contarte sobre cómo funcionamos."
            sesion['estado'] = 'mostrando_servicios'
        
        elif intencion == 'info_general':
            response_text = """🌍 **Sobre Sparks IoT & Energy**

Somos una **empresa de ingeniería** especializada en soluciones tecnológicas para energía, automatización e Industria 4.0 en Ecuador.

**🎯 Nuestro Enfoque:**
• Proyectos de ingeniería eléctrica, electrónica y automatización
• Orientados a eficiencia energética y digitalización industrial
• Generación renovable y reducción de huella de carbono

**💡 Objetivo:**
Reducir costos operativos, mejorar desempeño y apoyar la transición hacia un futuro más limpio para empresas, instituciones y hogares.

**🏆 Proyectos Destacados:**
• Sistema Off-Grid 5 kWh con paneles bifaciales (El Carmen, Manabí)
• Solar On-Grid 9 kW - Lavadora y Lubricadora J (Manta)
• Infraestructura fotovoltaica para EPAM (Empresa Pública de Aguas Manta)
• Bombeo Solar 6.5 kW desde 60m de profundidad (Comuna Liguiqui)
• Sistemas híbridos residenciales hasta 10 kWh de almacenamiento
• Automatización solar en Liguiqui (seguridad, cámaras, portero automático)

**🤝 Alianzas Tecnológicas:**
Trabajamos con marcas líderes como Growatt, Siemens y fabricantes Tier 1 para garantizar sistemas duraderos e inteligentes.

**📍 Ubicación:**
Edificio Manta Business Center, Torre B, Piso 3, Oficina 301
Av. Malecón (frente a Mall del Pacífico y Hotel Oro Verde)
Manta – Manabí – Ecuador

**📞 Contacto:**
• Teléfonos: +593 982840675 / +593 984141479
• WhatsApp: +593 985937244
• Email: info@sparksenergy.io
• Web: sparksenergy.io

¿Te gustaría conocer nuestros servicios específicos o ver más proyectos?"""
            sesion['estado'] = 'presentacion'
        
        elif intencion == 'precio':
            response_text = """💰 **Cotización y Presupuestos**

Los costos de un sistema solar varían según múltiples factores:

**📊 Variables que determinan el precio:**
• **Tipo de instalación**: On-Grid, Off-Grid o Híbrido
• **Capacidad del sistema**: kW necesarios según tu consumo
• **Almacenamiento**: Con o sin baterías (litio vs plomo)
• **Ubicación**: Accesibilidad, tipo de tejado, distancia
• **Componentes**: Marcas premium vs estándar
• **Complejidad**: Instalación residencial vs industrial

**📈 Rangos referenciales:**
• Sistema residencial básico: Desde $2,500 USD
• Sistema comercial mediano: $8,000 - $20,000 USD
• Proyectos industriales: Cotización personalizada

**🎁 Lo que incluye:**
✓ Estudio energético integral (sin costo)
✓ Diseño personalizado del sistema
✓ Todos los equipos y materiales
✓ Instalación profesional certificada
✓ Tramitación de permisos
✓ Capacitación y puesta en marcha
✓ Garantías extendidas

**💡 Retorno de inversión:**
La mayoría de sistemas se pagan solos en 4-7 años con el ahorro en factura eléctrica.

Para una cotización precisa y personalizada, ofrecemos un **estudio técnico gratuito** donde evaluamos tu consumo actual y diseñamos el sistema ideal.

¿Te gustaría agendar tu asesoría técnica sin costo? Puedo conectarte por WhatsApp."""
            sesion['estado'] = 'ofreciendo_asesoria'
        
        elif intencion == 'contacto':
            response_text = """📞 **Contáctanos por WhatsApp**

Puedo conectarte directamente con nuestro equipo técnico.

Dime qué servicio te interesa y te redirigiré inmediatamente a WhatsApp para que un especialista te atienda:

☀️ Instalaciones Solares
💧 Sistemas de Bombeo
💡 Iluminación Solar
📊 Eficiencia Energética
🏭 Industria 4.0

¿Cuál te interesa?"""
            sesion['estado'] = 'esperando_servicio_contacto'
        
        elif intencion == 'instalacion':
            response_text = """🔧 **Proceso de Instalación - ¿Cómo funciona?**

La **instalación de un sistema solar** es el proceso de montar y conectar todos los componentes necesarios para generar energía limpia. Esto incluye paneles solares, inversores, estructuras de montaje, cableado y sistemas de protección.

**Nuestro proceso profesional:**

1️⃣ **Visita Técnica Gratuita**
   📐 Evaluamos tu tejado/terreno, orientación solar
   📊 Medimos tu consumo eléctrico actual
   ☀️ Analizamos la radiación solar de tu zona

2️⃣ **Propuesta Personalizada**
   🎯 Diseñamos el sistema ideal para tus necesidades
   💰 Cotización detallada con ROI y ahorro mensual
   📋 Simulación de producción energética

3️⃣ **Instalación Profesional**
   🔨 Montaje de estructura y paneles
   ⚡ Instalación de inversor y protecciones
   🔌 Conexión al sistema eléctrico
   ⏱️ Duración: 2-5 días según tamaño

4️⃣ **Puesta en Marcha**
   ✅ Pruebas de funcionamiento
   📚 Capacitación de uso y monitoreo
   📄 Entrega de documentación técnica

5️⃣ **Seguimiento Post-Venta**
   📡 Monitoreo remoto del sistema
   🛠️ Soporte técnico continuo
   🔍 Mantenimientos preventivos

¿Te gustaría que un técnico visite tu ubicación para evaluar tu caso? Puedo conectarte por WhatsApp."""
            sesion['estado'] = 'ofreciendo_visita'
        
        elif intencion == 'tiempo':
            response_text = """⏱️ **Tiempos de Implementación - Planifica tu proyecto**

Cada proyecto solar tiene diferentes **fases** que requieren tiempo específico. Es importante conocer estos plazos para planificar tu inversión.

**📅 Cronograma Típico:**

🔍 **Evaluación Inicial:** 24-48 horas
   → Visita técnica para análisis del sitio
   → Qué hacemos: medición de espacio, consumo, viabilidad

📋 **Diseño y Propuesta:** 3-5 días hábiles
   → Ingeniería del sistema personalizado
   → Qué incluye: planos, equipos, presupuesto, simulación

🔨 **Instalación Física:**
   • **Residencial** (2-5 kW): 2-3 días
     Ideal para casas, pequeños negocios
   
   • **Comercial** (5-20 kW): 5-7 días
     Para oficinas, talleres, comercios medianos
   
   • **Industrial** (20+ kW): 2-3 semanas
     Grandes instalaciones, naves industriales

📄 **Trámites y Permisos:** 2-4 semanas
   Solo para sistemas conectados a la red eléctrica
   → Permisos municipales
   → Homologación con empresa eléctrica
   → Inspecciones y aprobaciones

**¿Por qué varía el tiempo?**
✓ Tamaño y complejidad del sistema
✓ Tipo de estructura (tejado, suelo, industrial)
✓ Disponibilidad de equipos importados
✓ Clima y temporada
✓ Permisos gubernamentales

💡 **Tip:** La mayoría de proyectos residenciales están operativos en 3-4 semanas desde el primer contacto.

¿Deseas iniciar el proceso? Puedo conectarte con un asesor por WhatsApp para coordinar tu visita."""
            sesion['estado'] = 'ofreciendo_visita'
        
        elif intencion == 'ubicacion':
            response_text = """📍 **Ubicación y Zona de Cobertura**

La **ubicación geográfica** es crucial en proyectos solares porque determina:

☀️ **Radiación Solar Disponible**
   Ecuador tiene excelente radiación, pero varía por región
   La costa tiene ~4.5-5.5 kWh/m²/día (muy bueno para solar)

🚚 **Logística y Soporte**
   Cercanía con nuestros técnicos reduce tiempos y costos
   Garantiza respuesta rápida ante cualquier eventualidad

🏗️ **Normativas Locales**
   Cada municipio tiene regulaciones específicas
   Conocemos los procesos y requisitos en nuestra zona

**🏢 Nuestra Oficina Principal:**
📍 **Edificio Manta Business Center**
   Torre B, Piso 3, Oficina 301
   Av. Malecón (frente a Mall del Pacífico y Hotel Oro Verde)
   Manta – Manabí – Ecuador

**🗺️ Zonas de Atención:**

✅ **Cobertura Total** (servicio completo):
   🔹 **Manta** - Base de operaciones
   🔹 Portoviejo
   🔹 Montecristi  
   🔹 Jaramijó
   🔹 Crucita, San Mateo, San Jacinto
   🔹 El Carmen
   🔹 Liguiqui
   🔹 Toda la provincia de Manabí

✅ **Proyectos Especiales**:
   🔸 Otras provincias de Ecuador
   🔸 Sistemas industriales (+50 kW)
   🔸 Instalaciones comerciales grandes

**📞 Canales de Contacto:**
• WhatsApp: +593 985937244
• Teléfonos: +593 982840675 / +593 984141479
• Email: info@sparksenergy.io
• Web: sparksenergy.io

💡 **¿Estás fuera de Manabí?**
Evaluamos proyectos en todo Ecuador. Instalaciones industriales y comerciales grandes justifican movilización nacional.

¿Tu proyecto está en nuestra zona? Cuéntame tu ubicación y te confirmo. También puedo conectarte directamente por WhatsApp."""
            sesion['estado'] = 'consultando_ubicacion'
        
        elif intencion == 'garantia':
            response_text = """🛡️ **Garantías y Respaldo - Tu inversión protegida**

Una **garantía** es el compromiso del fabricante o instalador de reparar o reemplazar un producto si falla. En energía solar, las garantías son extensas porque los equipos están diseñados para durar décadas.

**📦 Garantías de Equipos:**

☀️ **Paneles Solares: 25 años**
   → Qué cubre: Garantía de producción al 80% después de 25 años
   → Por qué es importante: Los paneles pierden ~0.5% eficiencia/año
   → Qué significa: Generarán energía por 30-40 años
   → Marcas: Trabajamos con Tier 1 (JA Solar, Trina, Canadian Solar)

⚡ **Inversores: 5-10 años**
   → Qué es: Convierte corriente continua (DC) a alterna (AC)
   → Qué cubre: Defectos de fabricación, fallas electrónicas
   → Extensiones: Algunas marcas ofrecen hasta 20 años
   → Nota: Es el componente que puede requerir reemplazo

🔋 **Baterías: 5-10 años o ciclos**
   → Qué es: Almacena energía para uso nocturno
   → Qué cubre: Capacidad mínima garantizada por ciclos
   → Tipos: Litio (10 años/6000 ciclos) vs Plomo (5 años/1500 ciclos)

🔩 **Estructura de Montaje: 10 años**
   → Qué cubre: Corrosión, deformaciones, desprendimientos
   → Material: Aluminio o acero galvanizado

**🔧 Garantía de Instalación:**

✅ **Mano de Obra: 2 años** (Sparks IoT&Energy)
   → Qué cubre: Filtraciones, conexiones, cableado
   → Incluye: Revisiones sin costo ante cualquier problema
   → Instaladores: Técnicos certificados con experiencia

✅ **Soporte Técnico:** Incluido de por vida
   → Asesoría telefónica/WhatsApp
   → Diagnóstico remoto de fallas
   → Actualización de software de inversores

**🛠️ Mantenimiento Preventivo:**

🔍 **¿Qué es?** Revisiones periódicas para optimizar rendimiento

**Incluye:**
   • Limpieza de paneles (2 veces/año recomendado)
   • Inspección de conexiones eléctricas
   • Verificación de tensiones y corrientes
   • Actualización de firmware
   • Monitoreo remoto 24/7 de producción

💰 **Planes disponibles:**
   • Plan Básico: 2 visitas/año
   • Plan Premium: 4 visitas/año + monitoreo

**📜 Certificaciones Internacionales:**
✓ IEC 61215 (paneles)
✓ IEC 61730 (seguridad)
✓ ISO 9001 (calidad)
✓ TUV, CE (certificaciones europeas)

¿Deseas más detalles sobre algún componente específico o las condiciones de garantía? Puedo conectarte con un asesor técnico por WhatsApp."""
            sesion['estado'] = 'ofreciendo_asesoria'
        
        # Manejadores para estados específicos
        elif sesion['estado'] == 'esperando_servicio_contacto':
            # El usuario está respondiendo después de preguntarle qué servicio le interesa
            servicio_encontrado = None
            for key, servicio in SERVICIOS.items():
                if any(keyword in mensaje_lower for keyword in servicio['keywords']):
                    servicio_encontrado = servicio
                    sesion['servicio_interes'] = key
                    break
            
            if servicio_encontrado:
                whatsapp_url = generar_mensaje_whatsapp(servicio_encontrado['nombre'])
                response_text = f"""¡Perfecto! 🎉

Te conectaré directamente con un especialista en **{servicio_encontrado['nombre']}** por WhatsApp.

📱 Al hacer clic en el botón verde, se abrirá WhatsApp con tu mensaje prellenado:
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
            if 'si' in mensaje_lower or 'claro' in mensaje_lower or 'ok' in mensaje_lower or 'dale' in mensaje_lower:
                whatsapp_url = generar_mensaje_whatsapp(
                    sesion.get('servicio_interes', 'Consulta general'),
                    "Solicito agendar una visita técnica."
                )
                response_text = """¡Excelente! 👍

Te conectaré con nuestro equipo técnico por WhatsApp para coordinar tu visita.

Ellos se pondrán en contacto contigo en las próximas horas para:
✅ Confirmar tu ubicación
✅ Acordar fecha y hora
✅ Preparar el estudio preliminar

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
            if 'si' in mensaje_lower or 'claro' in mensaje_lower or 'ok' in mensaje_lower or 'dale' in mensaje_lower or 'whatsapp' in mensaje_lower:
                servicio_nombre = SERVICIOS.get(sesion.get('servicio_interes', ''), {}).get('nombre', 'Asesoría técnica')
                whatsapp_url = generar_mensaje_whatsapp(servicio_nombre, "Solicito asesoría técnica detallada.")
                response_text = """¡Perfecto! 🎯

Te conectaré con un asesor técnico especializado por WhatsApp.

Nuestro equipo revisará tu caso y te ofrecerá:
📋 Asesoría técnica personalizada
💰 Cotización detallada
📊 Análisis de ahorro energético
🔧 Recomendaciones específicas

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
            # Capturar la ubicación mencionada
            ubicacion_mencionada = mensaje
            sesion['datos_usuario']['ubicacion'] = ubicacion_mencionada
            
            whatsapp_url = generar_mensaje_whatsapp(
                "Consulta sobre cobertura",
                f"Mi ubicación es: {ubicacion_mencionada}. ¿Pueden atenderme?"
            )
            response_text = f"""Gracias por compartir tu ubicación: **{ubicacion_mencionada}** 📍

Te conectaré con nuestro equipo comercial por WhatsApp para:
✅ Confirmar cobertura en tu zona
✅ Coordinar visita técnica
✅ Brindarte información específica de tu región

Haz clic en el botón verde de WhatsApp."""
            sesion['estado'] = 'redirigiendo_whatsapp'
        
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