// Configuration for MamaCare API endpoints
const config = {
    // Development configuration (localhost)
    development: {
        apiBaseUrl: 'http://localhost:5000',
        environment: 'development'
    },
    
    // Production configuration (Render)
    production: {
        apiBaseUrl: 'https://mamacare-backend.onrender.com', // Update this with your actual Render URL
        environment: 'production'
    }
};

// Determine which configuration to use
const isDevelopment = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1' ||
                     window.location.hostname.includes('localhost');

// Export the current configuration
const currentConfig = isDevelopment ? config.development : config.production;

// Make it available globally
window.MamaCareConfig = currentConfig;

// Helper function to get API URL
function getApiUrl(endpoint) {
    return `${currentConfig.apiBaseUrl}${endpoint}`;
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { config, currentConfig, getApiUrl };
} 