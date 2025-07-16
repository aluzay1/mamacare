// Reusable Feedback UI System for MamaCare
// This file provides consistent feedback messages across all pages

// Success message function
function showSuccessMessage(message, fields = []) {
    // Remove any existing success message
    const existingMessage = document.getElementById('customSuccessMessage');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create success message container
    const successContainer = document.createElement('div');
    successContainer.id = 'customSuccessMessage';
    successContainer.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        z-index: 10000;
        max-width: 400px;
        font-family: 'Poppins', sans-serif;
        animation: slideInRight 0.5s ease-out;
        border-left: 5px solid #2E7D32;
    `;
    
    // Create header
    const header = document.createElement('div');
    header.style.cssText = `
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        font-weight: 600;
        font-size: 16px;
    `;
    header.innerHTML = `
        <i class="fas fa-check-circle" style="margin-right: 10px; font-size: 20px;"></i>
        ${message}
    `;
    
    // Create content if fields are provided
    let content = null;
    if (fields.length > 0) {
        content = document.createElement('div');
        content.style.cssText = `
            margin-bottom: 15px;
            line-height: 1.5;
        `;
        
        if (fields.length === 1) {
            content.innerHTML = `<strong>${fields[0]}</strong> has been updated.`;
        } else {
            content.innerHTML = `
                <strong>${fields.length} fields</strong> have been updated:<br>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    ${fields.map(field => `<li>${field}</li>`).join('')}
                </ul>
            `;
        }
    }
    
    // Create close button
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '✓ Got it';
    closeBtn.style.cssText = `
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.3s ease;
        width: 100%;
    `;
    
    closeBtn.onmouseover = () => {
        closeBtn.style.background = 'rgba(255,255,255,0.3)';
    };
    
    closeBtn.onmouseout = () => {
        closeBtn.style.background = 'rgba(255,255,255,0.2)';
    };
    
    closeBtn.onclick = () => {
        successContainer.style.animation = 'slideOutRight 0.5s ease-in';
        setTimeout(() => successContainer.remove(), 500);
    };
    
    // Add CSS animations if not already present
    if (!document.getElementById('feedbackAnimations')) {
        const style = document.createElement('style');
        style.id = 'feedbackAnimations';
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
            @keyframes slideInLeft {
                from { transform: translateX(-100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOutLeft {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(-100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Assemble the message
    successContainer.appendChild(header);
    if (content) {
        successContainer.appendChild(content);
    }
    successContainer.appendChild(closeBtn);
    
    // Add to page
    document.body.appendChild(successContainer);
    
    // Auto-remove after 8 seconds
    setTimeout(() => {
        if (successContainer.parentNode) {
            successContainer.style.animation = 'slideOutRight 0.5s ease-in';
            setTimeout(() => successContainer.remove(), 500);
        }
    }, 8000);
}

// Error message function
function showErrorMessage(message, details = '') {
    // Remove any existing error message
    const existingMessage = document.getElementById('customErrorMessage');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create error message container
    const errorContainer = document.createElement('div');
    errorContainer.id = 'customErrorMessage';
    errorContainer.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #f44336, #d32f2f);
        color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        z-index: 10000;
        max-width: 400px;
        font-family: 'Poppins', sans-serif;
        animation: slideInRight 0.5s ease-out;
        border-left: 5px solid #c62828;
    `;
    
    // Create header
    const header = document.createElement('div');
    header.style.cssText = `
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        font-weight: 600;
        font-size: 16px;
    `;
    header.innerHTML = `
        <i class="fas fa-exclamation-triangle" style="margin-right: 10px; font-size: 20px;"></i>
        ${message}
    `;
    
    // Create content if details are provided
    let content = null;
    if (details) {
        content = document.createElement('div');
        content.style.cssText = `
            margin-bottom: 15px;
            line-height: 1.5;
            font-size: 14px;
            opacity: 0.9;
        `;
        content.textContent = details;
    }
    
    // Create close button
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '✕ Close';
    closeBtn.style.cssText = `
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.3s ease;
        width: 100%;
    `;
    
    closeBtn.onmouseover = () => {
        closeBtn.style.background = 'rgba(255,255,255,0.3)';
    };
    
    closeBtn.onmouseout = () => {
        closeBtn.style.background = 'rgba(255,255,255,0.2)';
    };
    
    closeBtn.onclick = () => {
        errorContainer.style.animation = 'slideOutRight 0.5s ease-in';
        setTimeout(() => errorContainer.remove(), 500);
    };
    
    // Assemble the message
    errorContainer.appendChild(header);
    if (content) {
        errorContainer.appendChild(content);
    }
    errorContainer.appendChild(closeBtn);
    
    // Add to page
    document.body.appendChild(errorContainer);
    
    // Auto-remove after 10 seconds
    setTimeout(() => {
        if (errorContainer.parentNode) {
            errorContainer.style.animation = 'slideOutRight 0.5s ease-in';
            setTimeout(() => errorContainer.remove(), 500);
        }
    }, 10000);
}

// Warning message function
function showWarningMessage(message, details = '') {
    // Remove any existing warning message
    const existingMessage = document.getElementById('customWarningMessage');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create warning message container
    const warningContainer = document.createElement('div');
    warningContainer.id = 'customWarningMessage';
    warningContainer.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #ff9800, #f57c00);
        color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        z-index: 10000;
        max-width: 400px;
        font-family: 'Poppins', sans-serif;
        animation: slideInRight 0.5s ease-out;
        border-left: 5px solid #ef6c00;
    `;
    
    // Create header
    const header = document.createElement('div');
    header.style.cssText = `
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        font-weight: 600;
        font-size: 16px;
    `;
    header.innerHTML = `
        <i class="fas fa-exclamation-circle" style="margin-right: 10px; font-size: 20px;"></i>
        ${message}
    `;
    
    // Create content if details are provided
    let content = null;
    if (details) {
        content = document.createElement('div');
        content.style.cssText = `
            margin-bottom: 15px;
            line-height: 1.5;
            font-size: 14px;
            opacity: 0.9;
        `;
        content.textContent = details;
    }
    
    // Create close button
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '⚠ Got it';
    closeBtn.style.cssText = `
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.3s ease;
        width: 100%;
    `;
    
    closeBtn.onmouseover = () => {
        closeBtn.style.background = 'rgba(255,255,255,0.3)';
    };
    
    closeBtn.onmouseout = () => {
        closeBtn.style.background = 'rgba(255,255,255,0.2)';
    };
    
    closeBtn.onclick = () => {
        warningContainer.style.animation = 'slideOutRight 0.5s ease-in';
        setTimeout(() => warningContainer.remove(), 500);
    };
    
    // Assemble the message
    warningContainer.appendChild(header);
    if (content) {
        warningContainer.appendChild(content);
    }
    warningContainer.appendChild(closeBtn);
    
    // Add to page
    document.body.appendChild(warningContainer);
    
    // Auto-remove after 8 seconds
    setTimeout(() => {
        if (warningContainer.parentNode) {
            warningContainer.style.animation = 'slideOutRight 0.5s ease-in';
            setTimeout(() => warningContainer.remove(), 500);
        }
    }, 8000);
}

// Info message function
function showInfoMessage(message, details = '') {
    // Remove any existing info message
    const existingMessage = document.getElementById('customInfoMessage');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create info message container
    const infoContainer = document.createElement('div');
    infoContainer.id = 'customInfoMessage';
    infoContainer.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #2196F3, #1976D2);
        color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        z-index: 10000;
        max-width: 400px;
        font-family: 'Poppins', sans-serif;
        animation: slideInRight 0.5s ease-out;
        border-left: 5px solid #1565C0;
    `;
    
    // Create header
    const header = document.createElement('div');
    header.style.cssText = `
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        font-weight: 600;
        font-size: 16px;
    `;
    header.innerHTML = `
        <i class="fas fa-info-circle" style="margin-right: 10px; font-size: 20px;"></i>
        ${message}
    `;
    
    // Create content if details are provided
    let content = null;
    if (details) {
        content = document.createElement('div');
        content.style.cssText = `
            margin-bottom: 15px;
            line-height: 1.5;
            font-size: 14px;
            opacity: 0.9;
        `;
        content.textContent = details;
    }
    
    // Create close button
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = 'ℹ Got it';
    closeBtn.style.cssText = `
        background: rgba(255,255,255,0.2);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.3s ease;
        width: 100%;
    `;
    
    closeBtn.onmouseover = () => {
        closeBtn.style.background = 'rgba(255,255,255,0.3)';
    };
    
    closeBtn.onmouseout = () => {
        closeBtn.style.background = 'rgba(255,255,255,0.2)';
    };
    
    closeBtn.onclick = () => {
        infoContainer.style.animation = 'slideOutRight 0.5s ease-in';
        setTimeout(() => infoContainer.remove(), 500);
    };
    
    // Assemble the message
    infoContainer.appendChild(header);
    if (content) {
        infoContainer.appendChild(content);
    }
    infoContainer.appendChild(closeBtn);
    
    // Add to page
    document.body.appendChild(infoContainer);
    
    // Auto-remove after 8 seconds
    setTimeout(() => {
        if (infoContainer.parentNode) {
            infoContainer.style.animation = 'slideOutRight 0.5s ease-in';
            setTimeout(() => infoContainer.remove(), 500);
        }
    }, 8000);
}

// Remove all feedback messages
function clearAllFeedbackMessages() {
    const messages = [
        'customSuccessMessage',
        'customErrorMessage', 
        'customWarningMessage',
        'customInfoMessage'
    ];
    
    messages.forEach(id => {
        const message = document.getElementById(id);
        if (message) {
            message.remove();
        }
    });
} 