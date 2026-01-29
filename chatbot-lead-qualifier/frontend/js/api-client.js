// API Client

class ChatbotAPI {
    constructor(baseURL = 'http://localhost:5000/api') {
        this.baseURL = baseURL;
        this.sessionId = this.generateSessionId();
    }

    generateSessionId() {
        const stored = localStorage.getItem('chatbot_session_id');
        if (stored) return stored;
        
        const newId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('chatbot_session_id', newId);
        return newId;
    }

    async sendMessage(message) {
        try {
            const response = await fetch(`${this.baseURL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error sending message:', error);
            return {
                error: true,
                response: 'Lo siento, hubo un error al procesar tu mensaje. Por favor intenta de nuevo.',
                session_id: this.sessionId
            };
        }
    }

    async getSession() {
        try {
            const response = await fetch(`${this.baseURL}/session/${this.sessionId}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error getting session:', error);
            return { error: true };
        }
    }

    async getLeads() {
        try {
            const response = await fetch(`${this.baseURL}/leads`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error getting leads:', error);
            return { error: true, leads: [], total: 0 };
        }
    }

    resetSession() {
        localStorage.removeItem('chatbot_session_id');
        this.sessionId = this.generateSessionId();
    }
} JavaScript