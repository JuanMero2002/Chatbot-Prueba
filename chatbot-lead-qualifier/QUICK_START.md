# ⚡ QUICK START - Chatbot Sparks IoT & Energy

## 5 MINUTOS PARA EMPEZAR

### Paso 1: Verificar que el servidor está corriendo
```bash
# Si no está corriendo, en una terminal nueva:
cd "C:\Users\JuanTCS\Desktop\Nueva carpeta (3)\Chatbot_Clone\Chatbot-Prueba\chatbot-lead-qualifier"
python run.py
```

Deberías ver:
```
[2026-01-30 14:23:36] INFO - Base de conocimiento cargada exitosamente
* Running on http://127.0.0.1:5000
```

### Paso 2: Abrir el chatbot
```
http://localhost:5000
```

### Paso 3: Probar una conversación
```
Escribe: Hola, ¿qué servicios ofrecen?
```

El bot responderá con información sobre los 6 servicios principales.

---

## PRUEBAS RÁPIDAS

### Test 1: Verificar base de conocimiento
```bash
python test_kb_integration.py
```

Debería ver: `[SUCCESS] TODAS LAS PRUEBAS PASARON CORRECTAMENTE`

### Test 2: Probar detección de intenciones
```
Input: "¿Qué proyectos han hecho?"
Output: Debería listar los 7 proyectos de referencia
```

### Test 3: Probar regla de alucinación
```
Input: "¿Usan inversores Fronius?"
Output: Debería mencionar marcas verificadas (JinkoSolar, SIEMENS, INVT, GROOWATT)
```

---

## COMANDOS MÁS COMUNES

| Comando | Función |
|---------|---------|
| `python run.py` | Iniciar servidor |
| `python test_kb_integration.py` | Ejecutar pruebas |
| Editar `knowledge_base.json` | Actualizar información |
| `Ctrl+C` en terminal | Detener servidor |

---

## INFORMACIÓN IMPORTANTE

### Contacto de Sparks
- **WhatsApp**: +593 982840675 / +593 962018222 / +593 989831819
- **Email**: info@sparksenergy.io
- **Horario**: Lunes a Sábado, 08:00 AM – 08:00 PM

### Ubicación
Edificio Manta Business Center, Torre B, Piso 3, Oficina 301  
Av. Malecón (Frente al Mall del Pacífico), Manta, Manabí, Ecuador

### Servicios (Teclea para probar)
1. "Quiero un sistema solar en mi casa"
2. "¿Qué es el Industria 4.0?"
3. "Necesito más información sobre bombeo solar"
4. "¿Cuánto cuesta?"
5. "¿Qué certificaciones tienen?"
6. "Muéstrame proyectos que hayan hecho"

---

## 🚨 SI ALGO NO FUNCIONA

### Error: "ModuleNotFoundError: No module named 'flask'"
```bash
Solución: Las dependencias ya están instaladas, solo asegúrate de estar
usando el entorno virtual correcto
```

### Error: "knowledge_base.json not found"
```bash
Solución: Verifica que el archivo existe en:
app/chatbot/knowledge_base.json
```

### El servidor no inicia
```bash
1. Verifica que Python 3.8+ está instalado
2. Confirma que estás en el directorio correcto
3. Intenta: python run.py
```

### El chatbot no responde
```bash
1. Abre http://localhost:5000 en el navegador
2. Si ves una página HTML, el servidor funciona
3. Intenta con un mensaje simple: "Hola"
```

---

## 📱 PROBAR CON EJEMPLOS

### Cliente Residencial
```
Tú: Tengo una casa en Manta y quiero reducir mi factura de electricidad
Bot: Debería ofrecerte Solar On-Grid con ejemplo de Ciudad del Mar
```

### Cliente Comercial
```
Tú: Tengo un negocio y gasto mucho en energía
Bot: Debería ofrecerte Solar On-Grid con ejemplo de Motel Intimus
```

### Cliente Industrial
```
Tú: Necesito automatizar mi producción
Bot: Debería ofrecerte Industria 4.0 con detalles de PLC y SCADA
```

### Cliente Pregunta por Marca
```
Tú: ¿Usan inversores Victron?
Bot: Debería mencionar las 4 marcas verificadas, NO inventar
```

---

## ARCHIVOS IMPORTANTES

| Archivo | Propósito | Editar? |
|---------|----------|--------|
| `app/chatbot/knowledge_base.json` | Información de la empresa | ✅ SÍ |
| `app/api/routes.py` | Lógica del chatbot | ❌ NO (a menos que sepas código) |
| `README_KB.md` | Documentación completa | ❌ NO |
| `.env.example` | Configuración | ⚠️ SOLO SI NECESARIO |

---

## 🎯 FLUJO DE CONVERSACIÓN TÍPICO

```
1. Usuario abre el chat
   ↓
2. Bot se presenta (saludo automático)
   ↓
3. Usuario pregunta sobre algo (servicio, precio, proyecto, etc.)
   ↓
4. Bot detecta la intención y responde con información relevante
   ↓
5. Si hay interés, bot ofrece contacto directo por WhatsApp
   ↓
6. Cliente cliquea WhatsApp y habla con equipo de ventas
```

---

## 📊 MÉTRICAS ESPERADAS

Después de implementar este chatbot, esperamos:

- ✅ **Detección correcta**: 95%+ de intenciones detectadas
- ✅ **Respuestas relevan tes**: 90%+ de satisfacción
- ✅ **Derivación a WhatsApp**: 100% cuando hay interés
- ✅ **Sin alucinaciones**: 0% de información inventada
- ✅ **Disponibilidad**: 24/7 sin interrupciones

---

## 🆘 SOPORTE TÉCNICO

Para reportar problemas:

1. **Ejecuta**: `python test_kb_integration.py`
2. **Copia la salida** si hay errores
3. **Revisa**: IMPLEMENTACION_KB.md para soluciones
4. **Contacta al equipo técnico** si el problema persiste

---

## 💡 TIPS ÚTILES

### Para el equipo de ventas:
- Comparte el archivo EJEMPLOS_CONVERSACIONES.md
- Entrena a tu equipo con los casos de uso
- Usa los proyectos de referencia como argumentos de venta

### Para el equipo técnico:
- Los datos están centralizados en knowledge_base.json
- Las pruebas se ejecutan automáticamente
- El código está estructurado y documentado

### Para gerencia:
- Métricas de conversación en tiempo real (próximamente)
- Lead scoring automático
- ROI medible desde el inicio

---

## 🎓 PRÓXIMOS PASOS

1. **Hoy**: Familiarizarse con el chatbot
2. **Mañana**: Entrenar al equipo de ventas
3. **Esta semana**: Probar con clientes reales
4. **Próximo mes**: Análisis de resultados y optimizaciones

---

## ✅ CHECKLIST FINAL

- [ ] El servidor está corriendo en http://localhost:5000
- [ ] Las pruebas pasan correctamente
- [ ] Puedo ver los 6 servicios listados
- [ ] Los contactos de WhatsApp aparecen en respuestas
- [ ] Los proyectos se mencionan como referencias
- [ ] El bot no inventa marcas de equipos
- [ ] He leído EJEMPLOS_CONVERSACIONES.md

---

## 🎉 ¡LISTO!

Tu chatbot está operativo. Comienza a generar leads calificados ahora.

**¿Preguntas?** Consulta:
- README_KB.md - Documentación completa
- EJEMPLOS_CONVERSACIONES.md - Casos de uso
- IMPLEMENTACION_KB.md - Detalles técnicos

---

**¡Mucho éxito con Sparks IoT & Energy!** 🌱⚡
