// Utility script to update hardcoded localhost URLs to use configurable API base URL
// This script should be run in the browser console to update URLs dynamically

function updateApiUrls() {
    // Get all script tags that contain fetch calls to localhost:5000
    const scripts = document.querySelectorAll('script');
    
    scripts.forEach(script => {
        if (script.textContent && script.textContent.includes('localhost:5000')) {
            // Replace hardcoded URLs with configurable ones
            script.textContent = script.textContent.replace(
                /http:\/\/localhost:5000/g, 
                '${window.MamaCareConfig.apiBaseUrl}'
            );
        }
    });
    
    // Also update any inline fetch calls
    const elements = document.querySelectorAll('*');
    elements.forEach(element => {
        if (element.textContent && element.textContent.includes('localhost:5000')) {
            element.textContent = element.textContent.replace(
                /http:\/\/localhost:5000/g, 
                '${window.MamaCareConfig.apiBaseUrl}'
            );
        }
    });
    
    console.log('API URLs updated to use configurable base URL');
}

// Function to create a fetch wrapper that uses the configurable base URL
function apiFetch(endpoint, options = {}) {
    const baseUrl = window.MamaCareConfig ? window.MamaCareConfig.apiBaseUrl : 'http://localhost:5000';
    const url = `${baseUrl}${endpoint}`;
    
    console.log(`Making API request to: ${url}`);
    
    return fetch(url, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    });
}

// Make the functions available globally
window.updateApiUrls = updateApiUrls;
window.apiFetch = apiFetch;

console.log('URL update utilities loaded. Use updateApiUrls() to update hardcoded URLs.');
console.log('Use apiFetch(endpoint, options) for making API calls with configurable base URL.'); 