# 🤖 Guía Completa de Interacciones del Chatbot Sparks IoT&Energy

## 📋 Índice
1. [Flujo Principal](#flujo-principal)
2. [Intenciones Detectadas](#intenciones-detectadas)
3. [Servicios Disponibles](#servicios-disponibles)
4. [Ejemplos de Conversaciones](#ejemplos-de-conversaciones)
5. [Estados de Conversación](#estados-de-conversación)

---

## 🎯 Flujo Principal

```
Usuario inicia conversación
    ↓
Saludo del Bot
    ↓
Usuario consulta servicios
    ↓
Bot muestra lista de servicios
    ↓
Usuario selecciona servicio
    ↓
Bot explica servicio detallado
    ↓
Bot pregunta si desea asesoría
    ↓
Usuario confirma (Sí)
    ↓
Bot genera enlace WhatsApp
    ↓
Usuario hace clic en WhatsApp
    ↓
Redirige a WhatsApp con mensaje pre-formateado
```

---

## 🧠 Intenciones Detectadas

### 1. **SALUDO**
**Palabras clave:** `hola`, `buenos`, `buenas`, `saludos`, `hey`, `hi`

**Respuesta del bot:**
```
¡Hola! 👋 Bienvenido a Sparks IoT&Energy.

🌱 Trabajamos por un mejor futuro para nuestro planeta a través de energías renovables en Manta, Manabí, Ecuador.

Nuestros servicios principales:
🔹 Eficiencia Energética
🔹 Energías Renovables
🔹 Industria 4.0

¿En qué puedo ayudarte hoy?
```

**Estado resultante:** `presentacion`

---

### 2. **CONSULTA DE SERVICIOS**
**Palabras clave:** `servicio`, `ofrecen`, `tienen`, `hacen`, `producto`

**Respuesta del bot:**
```
Excelente! Te cuento sobre nuestros servicios de energías renovables:

☀️ Solar Fotovoltaica Aislada (Off-Grid)
Sistemas autónomos sin conexión a red, ideales para zonas rurales.

⚡ Solar Fotovoltaica Conectada a Red (On-Grid)
Genera tu propia energía y reduce tu factura eléctrica.

💧 Sistemas de Bombeo Solar
Soluciones para riego y bombeo de agua optimizadas.

💡 Sistemas de Iluminación Solar
Iluminación LED para espacios públicos y privados.

📊 Eficiencia Energética
Auditorías y optimización de consumo.

🏭 Industria 4.0
Automatización y IoT para procesos industriales.

¿Sobre cuál servicio te gustaría conocer más?
```

**Estado resultante:** `mostrando_servicios`

---

### 3. **INFORMACIÓN GENERAL**
**Palabras clave:** `informacion`, `info`, `sobre`, `acerca`, `que es`

**Respuesta del bot:**
```
🌍 Sobre Sparks IoT&Energy

Somos una empresa comprometida con construir un mejor futuro mediante:

♻️ Energía solar fotovoltaica, solar térmica y mini eólica
🌱 Reducción de emisiones de CO2
💰 Ahorro en costos de energía eléctrica
⚡ Promoción de soberanía energética

¿Cómo funcionamos?
1️⃣ Estudio energético completo
2️⃣ Financiación y tramitación
3️⃣ Instalación y seguimiento

¿Te gustaría conocer nuestros servicios específicos?
```

**Estado resultante:** `presentacion`

---

### 4. **CONSULTA DE PRECIOS**
**Palabras clave:** `precio`, `costo`, `cotizacion`, `cuanto`, `valor`

**Respuesta del bot:**
```
Los costos varían según:
• Tipo de instalación
• Capacidad requerida
• Ubicación y características del sitio
• Componentes seleccionados

Para darte una cotización precisa, necesitamos realizar un estudio energético integral sin costo.

¿Te gustaría agendar una asesoría técnica gratuita?
```

**Estado resultante:** `ofreciendo_asesoria`

---

### 5. **SOLICITUD DE CONTACTO**
**Palabras clave:** `contacto`, `llamar`, `telefono`, `whatsapp`, `escribir`

**Respuesta del bot:**
```
📞 Contáctanos

¿Prefieres que te contactemos por WhatsApp?

Dime sobre qué servicio necesitas información y te redirigiré con un asesor especializado.
```

**Estado resultante:** `mostrando_servicios`

---

### 6. **CONFIRMACIÓN POSITIVA**
**Palabras clave:** `si`, `sí`, `claro`, `ok`, `dale`, `quiero`, `deseo`, `me interesa`, `afirmativo`

**Contexto requerido:** Estado = `esperando_confirmacion`

**Respuesta del bot:**
```
¡Perfecto! 🎉

Para brindarte la mejor atención personalizada, te invito a continuar la conversación por WhatsApp.

He preparado un mensaje para ti sobre: [Nombre del Servicio]

¿Deseas abrir WhatsApp ahora?
```

**Acción especial:** Genera botón de WhatsApp con URL pre-formateada

**Estado resultante:** `redirigiendo_whatsapp`

---

### 7. **CONFIRMACIÓN NEGATIVA**
**Palabras clave:** `no`, `nada`, `gracias`, `negativo`

**Contexto requerido:** Estado = `esperando_confirmacion`

**Respuesta del bot:**
```
No hay problema. ¿Hay algún otro servicio sobre el que quieras conocer más? O si prefieres, puedo contarte sobre cómo funcionamos.
```

**Estado resultante:** `mostrando_servicios`

---

## 🔆 Servicios Disponibles

### 1. **Solar Fotovoltaica Aislada (Off-Grid)**

**Palabras clave de detección:**
- `aislada`
- `off-grid`
- `sin red`
- `autonoma`
- `bateria`
- `rural`
- `remota`

**Descripción completa:**
```
📌 Solar Fotovoltaica o Híbrida Aislada (Off-grid)

Instalación solar que genera energía sin conexión a red. Ideal para zonas rurales con autonomía completa mediante baterías.

✅ Realizamos:
• Estudio energético integral
• Visitas técnicas
• Medición de patrones de consumo
• Proyección económica del ahorro
• Financiación y tramitación
• Instalación y seguimiento

¿Te gustaría que un asesor técnico se comunique contigo para brindarte más información sobre este servicio?
```

---

### 2. **Solar Fotovoltaica Conectada a Red (On-Grid)**

**Palabras clave de detección:**
- `conectada`
- `on-grid`
- `red`
- `factura`
- `ahorro`
- `excedente`

**Descripción completa:**
```
📌 Solar Fotovoltaica Conectada a Red (On-Grid)

Sistema conectado a red que permite generar tu propia energía e inyectar excedentes. Reduce tu factura eléctrica hasta alcanzar balance cero.

✅ Realizamos:
• Estudio energético integral
• Visitas técnicas
• Medición de patrones de consumo
• Proyección económica del ahorro
• Financiación y tramitación
• Instalación y seguimiento

¿Te gustaría que un asesor técnico se comunique contigo para brindarte más información sobre este servicio?
```

---

### 3. **Sistemas de Bombeo Solar**

**Palabras clave de detección:**
- `bombeo`
- `riego`
- `agua`
- `agricultura`
- `pozo`

**Descripción completa:**
```
📌 Sistemas de Bombeo Solar

Bombeo o riego fotovoltaico que reduce costos de electricidad. Optimizado con variadores de frecuencia para máximo rendimiento.

✅ Realizamos:
• Estudio energético integral
• Visitas técnicas
• Medición de patrones de consumo
• Proyección económica del ahorro
• Financiación y tramitación
• Instalación y seguimiento

¿Te gustaría que un asesor técnico se comunique contigo para brindarte más información sobre este servicio?
```

---

### 4. **Sistemas de Iluminación Solar**

**Palabras clave de detección:**
- `iluminacion`
- `luz`
- `led`
- `calle`
- `parque`
- `emergencia`

**Descripción completa:**
```
📌 Sistemas de Iluminación Solar

Iluminación LED solar para espacios públicos y privados. Ideal para parques, calles, emergencias con sensores de presencia.

✅ Realizamos:
• Estudio energético integral
• Visitas técnicas
• Medición de patrones de consumo
• Proyección económica del ahorro
• Financiación y tramitación
• Instalación y seguimiento

¿Te gustaría que un asesor técnico se comunique contigo para brindarte más información sobre este servicio?
```

---

### 5. **Eficiencia Energética**

**Palabras clave de detección:**
- `eficiencia`
- `optimizar`
- `consumo`
- `auditoria`
- `reducir`

**Descripción completa:**
```
📌 Eficiencia Energética

Optimización de tu consumo energético mediante auditorías y soluciones personalizadas para reducir costos.

✅ Realizamos:
• Estudio energético integral
• Visitas técnicas
• Medición de patrones de consumo
• Proyección económica del ahorro
• Financiación y tramitación
• Instalación y seguimiento

¿Te gustaría que un asesor técnico se comunique contigo para brindarte más información sobre este servicio?
```

---

### 6. **Industria 4.0**

**Palabras clave de detección:**
- `industria`
- `automatizacion`
- `iot`
- `procesos`
- `4.0`

**Descripción completa:**
```
📌 Industria 4.0

Automatización de procesos industriales con IoT y tecnologías inteligentes para mayor eficiencia.

✅ Realizamos:
• Estudio energético integral
• Visitas técnicas
• Medición de patrones de consumo
• Proyección económica del ahorro
• Financiación y tramitación
• Instalación y seguimiento

¿Te gustaría que un asesor técnico se comunique contigo para brindarte más información sobre este servicio?
```

---

## 💬 Ejemplos de Conversaciones Completas

### Ejemplo 1: Conversación Exitosa - Solar Conectada a Red

```
Usuario: Hola
Bot: ¡Hola! 👋 Bienvenido a Sparks IoT&Energy...

Usuario: ¿Qué servicios tienen?
Bot: Excelente! Te cuento sobre nuestros servicios de energías renovables...

Usuario: Me interesa la solar conectada a red
Bot: 📌 Solar Fotovoltaica Conectada a Red (On-Grid)...
     ¿Te gustaría que un asesor técnico se comunique contigo?

Usuario: Sí
Bot: ¡Perfecto! 🎉 Para brindarte la mejor atención...
     [MUESTRA BOTÓN DE WHATSAPP]

Usuario: [Hace clic en WhatsApp]
     → Redirige a WhatsApp con mensaje:
     "Hola, soy Cliente y deseo información sobre Solar Fotovoltaica Conectada a Red (On-Grid)"
```

---

### Ejemplo 2: Conversación - Consulta de Precios

```
Usuario: Hola, quisiera saber cuánto cuesta una instalación solar
Bot: Los costos varían según:
     • Tipo de instalación
     • Capacidad requerida...
     ¿Te gustaría agendar una asesoría técnica gratuita?

Usuario: Sí, me interesa
Bot: 📞 Contáctanos...
     Dime sobre qué servicio necesitas información...

Usuario: Solar para mi casa
Bot: 📌 Solar Fotovoltaica Conectada a Red (On-Grid)...
     ¿Te gustaría que un asesor técnico se comunique contigo?

Usuario: Claro
Bot: ¡Perfecto! 🎉...
     [MUESTRA BOTÓN DE WHATSAPP]
```

---

### Ejemplo 3: Conversación - Usuario Indeciso

```
Usuario: Hola
Bot: ¡Hola! 👋 Bienvenido a Sparks IoT&Energy...

Usuario: ¿Qué hacen?
Bot: 🌍 Sobre Sparks IoT&Energy
     Somos una empresa comprometida...

Usuario: Interesante, ¿qué servicios ofrecen?
Bot: Excelente! Te cuento sobre nuestros servicios...

Usuario: Me interesa el bombeo solar
Bot: 📌 Sistemas de Bombeo Solar...
     ¿Te gustaría que un asesor técnico se comunique contigo?

Usuario: No, primero quiero ver otras opciones
Bot: No hay problema. ¿Hay algún otro servicio sobre el que quieras conocer más?

Usuario: Sí, la iluminación solar
Bot: 📌 Sistemas de Iluminación Solar...
     ¿Te gustaría que un asesor técnico se comunique contigo?

Usuario: Sí
Bot: ¡Perfecto! 🎉...
     [MUESTRA BOTÓN DE WHATSAPP]
```

---

### Ejemplo 4: Conversación - Información General

```
Usuario: Hola
Bot: ¡Hola! 👋 Bienvenido a Sparks IoT&Energy...

Usuario: Cuéntame sobre ustedes
Bot: 🌍 Sobre Sparks IoT&Energy
     Somos una empresa comprometida con construir un mejor futuro...

Usuario: ¿Cómo funcionan?
Bot: 🌍 Sobre Sparks IoT&Energy...
     ¿Cómo funcionamos?
     1️⃣ Estudio energético completo
     2️⃣ Financiación y tramitación
     3️⃣ Instalación y seguimiento

Usuario: Perfecto, quiero contactarlos
Bot: 📞 Contáctanos...
```

---

## 📊 Estados de Conversación

### Estado: `inicial`
- **Descripción:** Estado por defecto cuando se crea una nueva sesión
- **Siguiente estado posible:** Cualquiera según la intención del usuario

### Estado: `presentacion`
- **Descripción:** Bot ha presentado la empresa
- **Acciones disponibles:** Consultar servicios, información general, precios

### Estado: `mostrando_servicios`
- **Descripción:** Bot mostró la lista de servicios disponibles
- **Acciones disponibles:** Seleccionar un servicio específico

### Estado: `esperando_confirmacion`
- **Descripción:** Bot explicó un servicio y espera confirmación del usuario
- **Acciones disponibles:** 
  - Confirmar (Sí) → Genera WhatsApp
  - Rechazar (No) → Vuelve a mostrar servicios

### Estado: `redirigiendo_whatsapp`
- **Descripción:** Bot generó enlace de WhatsApp
- **Acciones disponibles:** Usuario hace clic en botón de WhatsApp

### Estado: `ofreciendo_asesoria`
- **Descripción:** Bot ofrece asesoría técnica gratuita
- **Acciones disponibles:** Confirmar o consultar más información

---

## 🔗 Integración WhatsApp

### Formato del Mensaje WhatsApp

Cuando el usuario confirma interés en un servicio, el bot genera un enlace con el siguiente formato:

```
https://wa.me/593999999999?text=Hola,%20soy%20Cliente%20y%20deseo%20información%20sobre%20[Nombre%20del%20Servicio]
```

**Ejemplo real:**
```
https://wa.me/593999999999?text=Hola,%20soy%20Cliente%20y%20deseo%20información%20sobre%20Solar%20Fotovoltaica%20Conectada%20a%20Red%20(On-Grid)
```

### Configuración del Número de WhatsApp

**Ubicación:** `app/api/routes.py` línea 76

```python
numero_whatsapp = "593999999999"  # Cambiar por el número real
```

**Importante:** Actualizar este número con el WhatsApp real de la empresa Sparks IoT&Energy.

---

## 🎨 Interfaz del Usuario

### Elementos Visuales

1. **Widget de Chat Flotante**
   - Botón redondo en esquina inferior derecha
   - Badge con número de mensajes no leídos
   - Animación de apertura/cierre

2. **Mensajes del Bot**
   - Avatar con ícono de robot
   - Fondo blanco
   - Timestamp

3. **Mensajes del Usuario**
   - Avatar con ícono de usuario
   - Fondo morado (color primario)
   - Alineados a la derecha

4. **Botón WhatsApp**
   - Color verde característico (#25D366)
   - Ícono de WhatsApp
   - Animación al hover

5. **Indicador de Escritura**
   - Tres puntos animados
   - Aparece cuando el bot está "pensando"

---

## 🛠️ Personalización

### Cambiar Respuestas

**Archivo:** `app/api/routes.py`

Modificar las constantes en el diccionario `SERVICIOS`:

```python
SERVICIOS = {
    'solar_aislada': {
        'nombre': 'Nuevo Nombre del Servicio',
        'descripcion': 'Nueva descripción',
        'keywords': ['palabra1', 'palabra2']
    }
}
```

### Agregar Nuevo Servicio

1. Agregar al diccionario `SERVICIOS`
2. El sistema detectará automáticamente las keywords
3. Generará respuestas usando el template existente

### Modificar Intenciones

En la función `detectar_intencion()`, agregar o modificar:

```python
# Nueva intención
if any(word in mensaje for word in ['palabra1', 'palabra2']):
    return 'nueva_intencion'
```

Luego agregar el manejo en la función `chat()`:

```python
elif intencion == 'nueva_intencion':
    response_text = """Tu respuesta aquí"""
    sesion['estado'] = 'nuevo_estado'
```

---

## 📝 Notas Técnicas

### Almacenamiento de Sesiones
- **Actual:** En memoria (diccionario Python)
- **Recomendado para producción:** Redis o base de datos

### Generación de Session ID
- Formato: `session_[timestamp]_[random_string]`
- Almacenado en `localStorage` del navegador

### Detección de Intenciones
- Sistema basado en keywords (palabras clave)
- Case-insensitive (no distingue mayúsculas/minúsculas)
- Busca coincidencias parciales en el mensaje

---

## 🚀 Mejoras Futuras Sugeridas

1. **Reconocimiento de Nombres**
   - Extraer nombre del usuario del mensaje
   - Personalizar mensaje de WhatsApp

2. **NLP Avanzado**
   - Implementar NLTK o spaCy
   - Mejor comprensión de contexto

3. **Base de Datos**
   - Almacenar conversaciones
   - Analytics de leads

4. **Multi-idioma**
   - Detección automática de idioma
   - Respuestas en inglés/español

5. **Integración CRM**
   - Enviar leads automáticamente
   - Seguimiento de conversiones

6. **Horarios de Atención**
   - Respuestas automáticas fuera de horario
   - Programación de callbacks

---

## 📞 Soporte

Para modificaciones o consultas sobre el chatbot:
- Revisar código en `app/api/routes.py`
- Frontend en `frontend/js/chatbot-widget.js`
- Estilos en `frontend/css/chatbot-styles.css`

---

**Última actualización:** Enero 29, 2026  
**Versión:** 1.0.0
