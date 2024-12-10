document.addEventListener('DOMContentLoaded', function() {
    const chatButton = document.getElementById('chat-button');
    const chatWindow = document.getElementById('chat-window');
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const closeButton = document.getElementById('close-chat');

    // Mensaje inicial
    addBotMessage("👋 ¡Hola! Soy tu asistente de CV. Puedo ayudarte con:");
    addBotMessage("• Consejos para mejorar tu CV\n• Tips para la carta de presentación\n• Recomendaciones de habilidades\n• Orientación sobre secciones del CV\n\nEscribe 'ayuda' para ver todas las opciones.");

    chatButton.addEventListener('click', function() {
        chatWindow.style.display = 'block';
        chatButton.style.display = 'none';
        chatInput.focus();
    });

    closeButton.addEventListener('click', function() {
        chatWindow.style.display = 'none';
        chatButton.style.display = 'block';
    });

    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = chatInput.value.trim();
        
        if (message) {
            addUserMessage(message);
            chatInput.value = '';

            // Obtener respuesta del bot
            setTimeout(() => {
                let response = getBotResponse(message.toLowerCase());
                addBotMessage(response);
            }, 500);
        }
    });

    function addUserMessage(message) {
        const div = document.createElement('div');
        div.className = 'message user-message';
        div.textContent = message;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function addBotMessage(message) {
        const div = document.createElement('div');
        div.className = 'message bot-message';
        div.textContent = message;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function getBotResponse(message) {
        const responses = {
            'ayuda': `Puedo ayudarte con:\n• Consejos para CV\n• Carta de presentación\n• Sección de habilidades\n• Experiencia laboral\n• Educación y formación\n• Información personal\n\nSolo pregúntame sobre cualquiera de estos temas.`,
            
            'cv': `Consejos para un CV efectivo:\n1. Personaliza tu CV para cada puesto\n2. Usa palabras clave del anuncio de trabajo\n3. Destaca logros medibles\n4. Mantén un diseño limpio y profesional\n5. Revisa la ortografía\n6. Incluye solo información relevante`,
            
            'experiencia': `Para la experiencia laboral:\n• Usa el formato: puesto, empresa, fechas\n• Describe logros, no solo responsabilidades\n• Usa verbos de acción\n• Incluye métricas cuando sea posible\n• Ordena de más reciente a más antiguo`,
            
            'educación': `Para la sección de educación:\n• Incluye títulos relevantes\n• Menciona honores o reconocimientos\n• Añade cursos específicos si son relevantes\n• Lista certificaciones importantes\n• Incluye formación continua`,

            'habilidades': `Para la sección de habilidades:\n• Equilibra habilidades técnicas y blandas\n• Prioriza las más relevantes para el puesto\n• Incluye nivel de dominio\n• Actualízalas regularmente\n• Usa palabras clave del sector`,
            
            'información personal': `Tips para información personal:\n• Incluye solo datos necesarios\n• Asegura que el email sea profesional\n• Verifica que los teléfonos sean correctos\n• La foto debe ser profesional\n• Mantén la privacidad de datos sensibles`
        };

        for (let [key, value] of Object.entries(responses)) {
            if (message.includes(key)) {
                return value;
            }
        }

        return "No estoy seguro de cómo ayudarte con esa consulta. Prueba preguntando sobre 'cv', 'experiencia', 'habilidades', 'educación', o 'información personal', o escribe 'ayuda' para ver todas las opciones.";
    }
});