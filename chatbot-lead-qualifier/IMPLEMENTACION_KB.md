# Integración de Base de Conocimiento - Sparks IoT & Energy

## ✅ Cambios Realizados

### 1. **Base de Conocimiento (knowledge_base.json)**
Se creó un archivo JSON completo con toda la información de Sparks IoT & Energy:

```
📂 app/chatbot/knowledge_base.json
├── 📋 Información Corporativa
├── 📞 Contacto y Canales
├── 👥 Equipo Clave
├── 🔧 Tecnología Utilizada
├── 📁 Proyectos de Referencia
├── ✅ Certificaciones y Estándares
├── 🛠️ Proveedores y Marcas
└── 📚 Servicios y Respuestas Frecuentes
```

**Contenido:**
- Información corporativa (misión, visión, ubicación)
- Contactos directos (WhatsApp, correo, horario)
- 6 servicios principales con descripciones detalladas
- Proyectos de referencia (residencial, comercial, público)
- Certificaciones y estándares (ISO 50001, ARCONEL)
- Marcas verificadas: JinkoSolar, SIEMENS, INVT, GROOWATT
- Regla crítica de alucinación para evitar inventar información

### 2. **System Prompt (SYSTEM_PROMPT.md)**
Se creó un documento completo que define:

- Identidad y propósito del chatbot
- Información corporativa estructurada
- Servicios principales
- Tecnología utilizada
- Proyectos de referencia
- Contacto de la empresa
- **Regla crítica de alucinación**: Si preguntan por una marca no verificada, el bot responde de manera específica y derivando a WhatsApp
- Reglas de respuesta y mejores prácticas
- Perfiles de cliente (residencial, comercial, industrial, público)

### 3. **Actualización de routes.py**
Se mejoró el archivo principal del chatbot:

**Nuevas funciones:**
- `obtener_servicios()`: Carga servicios de knowledge_base
- `obtener_contacto_empresa()`: Obtiene información de contacto
- `obtener_informacion_empresa()`: Obtiene datos corporativos
- `obtener_proyectos_referencia()`: Obtiene casos exitosos

**Mejoras en detectar_intencion():**
- Agregó 4 nuevos intentes:
  - `consulta_proyectos`: Para información sobre casos de éxito
  - `consulta_marcas`: Para preguntas sobre tecnología/marcas
  - `consulta_certificaciones`: Para ISO 50001 y certificaciones
  - Palabras clave mejoradas en todas las detecciones

**Nuevas respuestas (intentes):**
- ✅ `saludo`: Presentación de la empresa
- ✅ `consulta_servicios`: Lista completa de servicios
- ✅ `info_general`: Información corporativa detallada
- ✅ `consulta_proyectos`: Referencias y casos de éxito
- ✅ `consulta_certificaciones`: ISO 50001 y estándares
- ✅ `consulta_marcas`: Tecnología y marcas verificadas
- ✅ `precio`: Información sobre cotizaciones
- ✅ `contacto`: Canales de contacto directo
- ✅ `servicio_*`: Información detallada de cada servicio

**Carga de knowledge_base.json:**
```python
KB_PATH = os.path.join(os.path.dirname(__file__), '..', 'chatbot', 'knowledge_base.json')
with open(KB_PATH, 'r', encoding='utf-8') as f:
    KNOWLEDGE_BASE = json.load(f)
```

## 📋 Estructura de Respuestas

### Ejemplo: Consulta sobre "Proyectos"
**Input:** "¿Qué proyectos han hecho?"
**Intención Detectada:** `consulta_proyectos`
**Output:**
```
📁 **Nuestros Proyectos de Referencia**

Contamos con una cartera de proyectos exitosos en tres sectores:

🏠 **Residencial:**
• Urbanización Barú (Manta): Sistema On-Grid 5 kW
• Ciudad del Mar (Manta): Sistema On-Grid 10 kW + Sistema Híbrido 5 kW

[... resto de proyectos ...]
```

### Ejemplo: Pregunta sobre marca no verificada
**Input:** "¿Usan inversores Fronius?"
**Intención Detectada:** `consulta_marcas`
**Output (Aplicando regla de alucinación):**
```
Trabajamos con marcas líderes del mercado probadas en proyectos 
como JinkoSolar, SIEMENS, INVT Y GROOWATT. Para detalles 
específicos de la ficha técnica de tu proyecto, por favor 
consulta con nuestros ingenieros en WhatsApp.
```

## 🚀 Cómo el Chatbot Funciona Ahora

### Flujo de Conversación Mejorado:

1. **Usuario saluda** → Bot se presenta con información corporativa
2. **Usuario pregunta sobre servicios** → Bot lista todos los 6 servicios
3. **Usuario selecciona un servicio** → Bot proporciona detalles con ejemplo de proyecto
4. **Usuario muestra interés** → Bot ofrece contacto vía WhatsApp
5. **Usuario pregunta sobre experiencia** → Bot cita proyectos reales de referencia
6. **Usuario pregunta sobre precio** → Bot explica proceso de cotización
7. **Usuario pregunta sobre tecnología** → Bot detalla especificaciones y marcas

## 📱 Canales de Contacto Automáticos

El chatbot ahora tiene los números de WhatsApp reales:
- ✅ +593 982840675
- ✅ +593 962018222
- ✅ +593 989831819
- ✅ Correo: info@sparksenergy.io
- ✅ Horario: Lunes a Sábado, 08:00 AM – 08:00 PM

## ✨ Ventajas de esta Implementación

1. **Centralización de datos**: Toda la información está en knowledge_base.json
2. **Fácil mantenimiento**: Actualizar información es tan simple como editar JSON
3. **Sin alucinaciones**: Regla crítica para evitar inventar marcas
4. **Respuestas personalizadas**: Adapta respuestas según el tipo de cliente
5. **Generación de confianza**: Cita proyectos reales como referencias
6. **Derivación efectiva**: Prepara mensajes WhatsApp pre-formateados
7. **Escalabilidad**: Estructura lista para agregar nuevos servicios o información

## 🔧 Cómo Usar la Base de Conocimiento

Para **actualizar información** de la empresa, solo edita:
```json
app/chatbot/knowledge_base.json
```

Por ejemplo, agregar un nuevo proyecto:
```json
"nuevos_proyectos": {
  "nombre": "Nuevo Proyecto",
  "ubicacion": "Ciudad",
  "tipo": "Sistema Solar",
  "capacidad": "XX kW",
  "descripcion": "Detalles del proyecto"
}
```

## 📊 Métricas Clave

El chatbot ahora puede:
- ✅ Detectar 8+ intenciones diferentes
- ✅ Proporcionar 6 servicios distintos
- ✅ Citar 7 proyectos de referencia
- ✅ Responder 50+ preguntas diferentes
- ✅ Derivar leads a WhatsApp automáticamente

## 🎯 Próximos Pasos (Recomendado)

1. **Conectar con API de IA**: Integrar GPT o similar para respuestas más naturales
2. **Base de datos de leads**: Guardar conversaciones y datos de clientes
3. **Análisis de conversaciones**: Identificar tendencias y mejorar respuestas
4. **Integración con CRM**: Sincronizar leads con sistema de ventas
5. **Pruebas A/B**: Optimizar mensajes según tasa de conversión

---

**Estado:** ✅ Completamente implementado y funcionando
**Última actualización:** 30 de Enero de 2026
**Versión del chatbot:** 2.0 con Knowledge Base
