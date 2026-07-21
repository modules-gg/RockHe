// ============================================
// RockHe — GiMi 0.1 Main App
// ============================================

const App = {
    mode: 'chat',      // 'chat' | 'code'
    history: [],       // Conversation history
    isGenerating: false,
    
    // DOM refs
    elements: {
        thread: null,
        input: null,
        sendBtn: null,
        status: null,
        tokenCount: null,
        modeChat: null,
        modeCode: null,
        clearBtn: null,
    },

    init() {
        this.cacheElements();
        this.bindEvents();
        this.updateStatus('Ready');
        console.log('🪨 RockHe GiMi 0.1 initialized');
    },

    cacheElements() {
        this.elements.thread = document.getElementById('chat-thread');
        this.elements.input = document.getElementById('message-input');
        this.elements.sendBtn = document.getElementById('send-btn');
        this.elements.status = document.getElementById('status');
        this.elements.tokenCount = document.getElementById('token-count');
        this.elements.modeChat = document.getElementById('mode-chat');
        this.elements.modeCode = document.getElementById('mode-code');
        this.elements.clearBtn = document.getElementById('clear-btn');
    },

    bindEvents() {
        // Send on Enter (Shift+Enter for newline)
        this.elements.input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        this.elements.input.addEventListener('input', () => {
            this.autoResize();
            this.updateSendButton();
        });

        this.elements.sendBtn.addEventListener('click', () => this.sendMessage());

        // Mode toggle
        this.elements.modeChat.addEventListener('click', () => this.setMode('chat'));
        this.elements.modeCode.addEventListener('click', () => this.setMode('code'));

        // Clear chat
        this.elements.clearBtn.addEventListener('click', () => this.clearChat());

        // Quick action buttons
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.elements.input.value = btn.dataset.prompt;
                this.autoResize();
                this.updateSendButton();
                this.sendMessage();
            });
        });
    },

    setMode(mode) {
        this.mode = mode;
        this.elements.modeChat.classList.toggle('active', mode === 'chat');
        this.elements.modeCode.classList.toggle('active', mode === 'code');
        
        const placeholder = mode === 'code' 
            ? 'Describe your coding task...' 
            : 'Ask GiMi anything...';
        this.elements.input.placeholder = placeholder;
    },

    autoResize() {
        const ta = this.elements.input;
        ta.style.height = 'auto';
        ta.style.height = Math.min(ta.scrollHeight, 200) + 'px';
    },

    updateSendButton() {
        const hasText = this.elements.input.value.trim().length > 0;
        this.elements.sendBtn.disabled = !hasText || this.isGenerating;
    },

    async sendMessage() {
        const text = this.elements.input.value.trim();
        if (!text || this.isGenerating) return;

        // Add user message to thread
        this.addMessage('user', text);
        this.elements.input.value = '';
        this.autoResize();
        this.updateSendButton();

        // Update history
        this.history.push({ role: 'user', content: text });

        // Show loading
        this.isGenerating = true;
        this.updateStatus('GiMi is thinking...');
        this.updateSendButton();

        const loadingId = this.addLoading();

        try {
            // Call API
            const endpoint = this.mode === 'code' ? '/code' : '/chat';
            const response = await ApiClient.send(endpoint, {
                message: text,
                history: this.history,
            });

            // Remove loading, add AI response
            this.removeLoading(loadingId);
            this.addMessage('ai', response.response);

            // Update history
            this.history.push({ role: 'assistant', content: response.response });

            this.updateStatus('Ready');
            this.updateTokenCount(response.tokens_used);

        } catch (err) {
            this.removeLoading(loadingId);
            this.addMessage('ai', `**Error:** ${err.message}`, true);
            this.updateStatus('Error');
        }

        this.isGenerating = false;
        this.updateSendButton();
    },

    addMessage(role, content, isError = false) {
        const msg = document.createElement('div');
        msg.className = `message ${role}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = role === 'user' ? 'You' : 'GiMi';
        
        const body = document.createElement('div');
        body.className = 'message-content';
        
        // Render Markdown
        body.innerHTML = MarkdownRenderer.render(content);
        
        // Syntax highlight code blocks
        body.querySelectorAll('pre code').forEach(block => {
            CodeBlock.highlight(block);
        });

        msg.appendChild(avatar);
        msg.appendChild(body);
        this.elements.thread.appendChild(msg);
        
        // Scroll to bottom
        this.elements.thread.scrollTop = this.elements.thread.scrollHeight;
    },

    addLoading() {
        const id = 'loading-' + Date.now();
        const msg = document.createElement('div');
        msg.id = id;
        msg.className = 'message ai';
        msg.innerHTML = `
            <div class="message-avatar">GiMi</div>
            <div class="message-content">
                <em>Thinking...</em>
            </div>
        `;
        this.elements.thread.appendChild(msg);
        this.elements.thread.scrollTop = this.elements.thread.scrollHeight;
        return id;
    },

    removeLoading(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    },

    clearChat() {
        this.history = [];
        this.elements.thread.innerHTML = `
            <div class="welcome">
                <h2>🪨 Welcome to RockHe</h2>
                <p>GiMi 0.1 — Local AI for coding and conversation.</p>
                <div class="quick-actions">
                    <button class="quick-btn" data-prompt="Explain recursion in Python">🐍 Recursion</button>
                    <button class="quick-btn" data-prompt="Write a REST API in FastAPI">⚡ FastAPI</button>
                    <button class="quick-btn" data-prompt="Debug this code: def add(a,b): return a-b">🐛 Debug</button>
                </div>
            </div>
        `;
        // Re-bind quick buttons
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.elements.input.value = btn.dataset.prompt;
                this.autoResize();
                this.updateSendButton();
                this.sendMessage();
            });
        });
        this.updateStatus('Ready');
        this.updateTokenCount(0);
    },

    updateStatus(text) {
        this.elements.status.textContent = text;
    },

    updateTokenCount(count) {
        this.elements.tokenCount.textContent = count > 0 ? `${count} tokens` : '0 tokens';
    },
};

// Start
document.addEventListener('DOMContentLoaded', () => App.init());
