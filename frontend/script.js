const chatContainer = document.getElementById('chat-container');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const clearBtn = document.getElementById('clear-btn');

// Backend URL - change this to your deployed backend URL
const BACKEND_URL = 'https://therapyai-model-production.up.railway.app'; // Railway deployment URL

let chatHistory = [];

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = content;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Add user message to UI
    addMessage(message, 'user');
    chatHistory.push([message, null]);

    // Clear input
    messageInput.value = '';

    try {
        const response = await fetch(`${BACKEND_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: chatHistory.slice(0, -1) // Exclude the current message
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to get response from server');
        }

        const data = await response.json();
        const assistantResponse = data.response;

        // Add assistant message to UI
        addMessage(assistantResponse, 'assistant');
        chatHistory[chatHistory.length - 1][1] = assistantResponse;
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, there was an error processing your message.', 'assistant');
    }
}

function clearChat() {
    chatContainer.innerHTML = '';
    chatHistory = [];
}

sendBtn.addEventListener('click', sendMessage);
clearBtn.addEventListener('click', clearChat);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
