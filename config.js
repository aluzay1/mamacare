// API Configuration
const API_CONFIG = {
    // Development - local backend
    development: 'http://localhost:5000',
    
    // Production - Render backend
    production: 'https://mamacare-backend-1bdm.onrender.com', // Update this with your actual Render URL
    
    // Get current environment
    getBaseUrl: function() {
        // Check if we're on Netlify (production)
        if (window.location.hostname.includes('netlify.app') || 
            window.location.hostname.includes('netlify.com') ||
            window.location.hostname === 'mamacare.netlify.app') {
            return this.production;
        }
        // Otherwise use development
        return this.development;
    }
};

// Helper function to make API calls
async function apiCall(endpoint, options = {}) {
    const baseUrl = API_CONFIG.getBaseUrl();
    const url = `${baseUrl}${endpoint}`;
    
    console.log(`Making API call to: ${url}`);
    
    // Prepare headers
    let headers = {
        'Accept': 'application/json',
        ...options.headers
    };
    
    // Only set Content-Type if it's not FormData
    // For FormData, let the browser set the correct content-type with boundary
    if (!(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }
    
    const response = await fetch(url, {
        ...options,
        headers: headers
    });
    
    return response;
} 