document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('flash-messages-container');
    if (!container) return;

    const messages = JSON.parse(container.dataset.messages);
    
    messages.forEach(([category, message]) => {
        // Create popup element
        const popup = document.createElement('div');
        popup.className = `flash-popup flash-${category}`;
        popup.textContent = message;
        
        // Add to body
        document.body.appendChild(popup);
        
        // Trigger animation
        setTimeout(() => popup.classList.add('show'), 10);
        
        // Remove after 3 seconds
        setTimeout(() => {
            popup.classList.remove('show');
            setTimeout(() => popup.remove(), 500); // Wait for fadeout animation
        }, 3000);
    });
});