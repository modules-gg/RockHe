// ============================================
// RockHe — GiMi 0.1 API Client
// ============================================

const ApiClient = {
    // Base URL for local API server
    // Change this if hosting API elsewhere
    baseUrl: 'http://localhost:8000',

    /**
     * Send a message to the RockHe API.
     * 
     * @param {string} endpoint - '/chat' or '/code'
     * @param {Object} payload - { message, history, ... }
     * @returns {Promise<Object>} - API response
     */
    async send(endpoint, payload) {
        const url = `${this.baseUrl}${endpoint}`;

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || `HTTP ${response.status}`);
            }

            return await response.json();

        } catch (err) {
            // Network error or CORS issue
            if (err.name === 'TypeError' && err.message.includes('fetch')) {
                throw new Error(
                    'Cannot connect to RockHe API. ' +
                    'Make sure the server is running on ' + this.baseUrl
                );
            }
            throw err;
        }
    },

    /**
     * Health check — ping the server.
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseUrl}/`);
            return await response.json();
        } catch {
            return null;
        }
    },
};
