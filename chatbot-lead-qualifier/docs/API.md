# Documentación API

## Endpoints

### Chatbot
- `POST /api/chat/message` - Enviar mensaje al chatbot
- `GET /api/chat/conversation/:id` - Obtener conversación
- `POST /api/chat/conversation` - Crear nueva conversación

### Lead Qualification
- `POST /api/leads/qualify` - Calificar un lead
- `GET /api/leads/:id` - Obtener información del lead
- `PUT /api/leads/:id` - Actualizar información del lead

### WhatsApp Integration
- `POST /api/whatsapp/send` - Enviar mensaje por WhatsApp
- `POST /api/whatsapp/webhook` - Webhook para mensajes entrantes

## Autenticación

Usar API Key en header: `Authorization: Bearer YOUR_API_KEY`

