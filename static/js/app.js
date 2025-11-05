// Chat application JavaScript
class ChatApp {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.clearButton = document.getElementById('clearButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.statusIndicator = document.getElementById('statusIndicator');
        this.modelInfo = document.getElementById('modelInfo');
        this.typingMessages = [
            'Thinking...',
            'Retrieving context...',
            'Analyzing conversation history...',
            'Generating response...'
        ];
        this.currentTypingIndex = 0;
        this.typingInterval = null;
        
        this.init();
    }

    init() {
        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
            this.updateSendButton();
        });

        // Send message on Enter (Shift+Enter for new line)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());

        // Clear button click
        this.clearButton.addEventListener('click', () => this.clearHistory());

        // Check status on load
        this.checkStatus();

        // Update send button initially
        this.updateSendButton();
    }

    updateSendButton() {
        const hasText = this.messageInput.value.trim().length > 0;
        this.sendButton.disabled = !hasText;
    }

    async checkStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            if (data.success) {
                this.updateStatus(data.ollama_running);
                if (data.model) {
                    this.modelInfo.textContent = `Model: ${data.model} ${data.rag_enabled ? '(RAG Enabled)' : ''}`;
                }
            }
        } catch (error) {
            console.error('Status check failed:', error);
            this.updateStatus(false);
        }
    }

    updateStatus(isConnected) {
        const statusDot = this.statusIndicator.querySelector('.status-dot');
        const statusText = this.statusIndicator.querySelector('.status-text');
        
        if (isConnected) {
            statusDot.classList.add('connected');
            statusText.textContent = 'Connected';
        } else {
            statusDot.classList.remove('connected');
            statusText.textContent = 'Disconnected';
        }
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        this.addMessage('user', message);
        
        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        this.updateSendButton();

        // Show typing indicator with rotating messages
        this.addTypingIndicator();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });

            const data = await response.json();
            this.removeTypingIndicator();

            if (data.success) {
                this.addMessage('assistant', data.response, data.model);
            } else {
                this.addMessage('assistant', `Error: ${data.error || 'Failed to get response'}`);
            }
        } catch (error) {
            this.removeTypingIndicator();
            this.addMessage('assistant', `Error: ${error.message || 'Network error occurred'}`);
        }
    }

    addMessage(type, content, model = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = content;
        
        const meta = document.createElement('div');
        meta.className = 'message-meta';
        
        const time = new Date().toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
        meta.innerHTML = `<span class="message-time">${time}</span>`;
        
        if (model && type === 'assistant') {
            meta.innerHTML += `<span>🤖 ${model}</span>`;
        }
        
        messageDiv.appendChild(bubble);
        messageDiv.appendChild(meta);
        
        // Remove welcome message if it exists
        const welcomeMessage = this.chatMessages.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => welcomeMessage.remove(), 300);
        }
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Typewriter effect for assistant messages
        if (type === 'assistant') {
            this.typewriterEffect(bubble, content);
        }
    }

    typewriterEffect(element, text) {
        element.textContent = '';
        let index = 0;
        
        const type = () => {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                index++;
                setTimeout(type, 20); // Adjust speed here (lower = faster)
            }
        };
        
        type();
    }

    addTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant typing-message';
        typingDiv.id = 'typingIndicator';
        
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        
        const textSpan = document.createElement('span');
        textSpan.className = 'typing-text';
        textSpan.textContent = this.typingMessages[0];
        
        const dotsContainer = document.createElement('div');
        dotsContainer.className = 'typing-dots';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.className = 'typing-dot';
            dotsContainer.appendChild(dot);
        }
        
        indicator.appendChild(textSpan);
        indicator.appendChild(dotsContainer);
        typingDiv.appendChild(indicator);
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
        
        // Rotate through typing messages
        this.currentTypingIndex = 0;
        this.typingInterval = setInterval(() => {
            this.currentTypingIndex = (this.currentTypingIndex + 1) % this.typingMessages.length;
            const typingText = typingDiv.querySelector('.typing-text');
            if (typingText) {
                typingText.textContent = this.typingMessages[this.currentTypingIndex];
            }
        }, 2000); // Change message every 2 seconds
    }

    removeTypingIndicator() {
        // Clear the interval
        if (this.typingInterval) {
            clearInterval(this.typingInterval);
            this.typingInterval = null;
        }
        
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => typingIndicator.remove(), 300);
        }
    }

    async clearHistory() {
        if (!confirm('Are you sure you want to clear the conversation history?')) {
            return;
        }

        try {
            const response = await fetch('/api/clear', {
                method: 'POST',
            });

            const data = await response.json();
            
            if (data.success) {
                // Remove all messages except welcome
                const messages = this.chatMessages.querySelectorAll('.message');
                messages.forEach(msg => {
                    msg.style.animation = 'fadeOut 0.3s ease-out';
                    setTimeout(() => msg.remove(), 300);
                });
                
                // Show welcome message again
                setTimeout(() => {
                    this.showWelcomeMessage();
                }, 300);
            }
        } catch (error) {
            console.error('Clear history failed:', error);
            alert('Failed to clear history');
        }
    }

    showWelcomeMessage() {
        const welcomeDiv = document.createElement('div');
        welcomeDiv.className = 'welcome-message';
        welcomeDiv.innerHTML = `
            <div class="welcome-icon">🚀</div>
            <h2>Welcome to Release Dashboard AI Assistant</h2>
            <p>I'm your AI assistant for the Release Dashboard project. Ask me anything about releases, patches, Jira tickets, database backups, or any project-related questions. I'll use context from previous conversations to provide accurate answers.</p>
            <div class="feature-tags">
                <span class="tag">🔍 RAG Enabled</span>
                <span class="tag">🧠 Local LLM</span>
                <span class="tag">💬 Context-Aware</span>
                <span class="tag">📊 Release Dashboard</span>
            </div>
        `;
        this.chatMessages.appendChild(welcomeDiv);
    }

    scrollToBottom() {
        this.chatMessages.scrollTo({
            top: this.chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }
}

// Add fadeOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-10px);
        }
    }
`;
document.head.appendChild(style);

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});

