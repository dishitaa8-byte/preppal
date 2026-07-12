document.addEventListener('DOMContentLoaded', () => {
    // Check if it's the user's first visit
    const isFirstVisit = localStorage.getItem('preppal_first_visit') === null;

    // Get DOM elements
    const welcomeText = document.getElementById('welcome-text');
    const tagline = document.getElementById('tagline');
    const divider = document.getElementById('divider');
    const actionSection = document.getElementById('action-section');
    const attachBtn = document.getElementById('attach-btn');
    const fileInput = document.getElementById('file-input');
    const topicInput = document.getElementById('topic-input');
    const fileDisplay = document.getElementById('file-display');
    const fileName = document.getElementById('file-name');
    const removeFileBtn = document.getElementById('remove-file-btn');
    const startBtn = document.getElementById('start-btn');

    if (isFirstVisit) {
        // First visit: play the intro animation
        playIntroAnimation(welcomeText, tagline, divider, actionSection);
        // Set flag in localStorage to not show intro again
        localStorage.setItem('preppal_first_visit', 'false');
    } else {
        // Returning visit: show everything immediately
        showAllElements(welcomeText, tagline, divider, actionSection);
    }

    // Attach button click handler
    if (attachBtn && fileInput) {
        attachBtn.addEventListener('click', () => {
            fileInput.click();
        });
    }

    // File input change handler
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                handleFileSelect(file);
            }
        });
    }

    // Remove file button handler
    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', () => {
            handleFileRemove();
        });
    }

    // Start Prep button click handler
    if (startBtn) {
        startBtn.addEventListener('click', async () => {
            await startSession();
        });
    }
    
    // Start session function
    async function startSession() {
        const topicInput = document.getElementById('topic-input');
        const fileInput = document.getElementById('file-input');
        
        // Show loading state on button
        startBtn.disabled = true;
        startBtn.innerHTML = '<span class="btn-icon">⚡</span> Starting...';
        
        try {
            const formData = new FormData();
            
            // Add topic
            if (topicInput && topicInput.value.trim()) {
                formData.append('topic', topicInput.value.trim());
            }
            
            // Add file
            if (fileInput && fileInput.files.length > 0) {
                formData.append('pdf', fileInput.files[0]);
            }
            
            const response = await fetch('/api/start', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.error) {
                alert(data.error);
                return;
            }
            
            // Redirect to loading page (questions generated there)
            window.location.href = `/prep/${data.session_id}/loading`;
        } catch (error) {
            console.error('Error starting session:', error);
            alert('Failed to start session');
        } finally {
            // Re-enable button
            startBtn.disabled = false;
            startBtn.innerHTML = '<span class="btn-icon">⚡</span> Start Prep';
        }
    }
});

/**
 * Plays the first visit intro animation
 * @param {HTMLElement} welcomeText - Welcome text element
 * @param {HTMLElement} tagline - Tagline element
 * @param {HTMLElement} divider - Divider element
 * @param {HTMLElement} actionSection - Action section (cards + button) element
 */
function playIntroAnimation(welcomeText, tagline, divider, actionSection) {
    // Step 1: After 0.8 seconds, show welcome text
    setTimeout(() => {
        if (welcomeText) {
            welcomeText.classList.add('visible');
        }
    }, 800);

    // Step 2: After another 1 second (total 1.8s), show tagline
    setTimeout(() => {
        if (tagline) {
            tagline.classList.add('visible');
        }
    }, 1800);

    // Step 3: After another 0.5 seconds (total 2.3s), show divider and action section
    setTimeout(() => {
        if (divider) {
            divider.classList.add('visible');
        }
        if (actionSection) {
            actionSection.classList.add('visible');
        }
    }, 2300);
}

/**
 * Shows all elements immediately for returning visitors
 * @param {HTMLElement} welcomeText - Welcome text element
 * @param {HTMLElement} tagline - Tagline element
 * @param {HTMLElement} divider - Divider element
 * @param {HTMLElement} actionSection - Action section element
 */
function showAllElements(welcomeText, tagline, divider, actionSection) {
    if (welcomeText) {
        welcomeText.classList.add('visible');
        welcomeText.style.display = 'none'; // Hide welcome text for returning visitors
    }
    if (tagline) {
        tagline.classList.add('visible');
    }
    if (divider) {
        divider.classList.add('visible');
    }
    if (actionSection) {
        actionSection.classList.add('visible');
    }
}

/**
 * Handles file selection
 * @param {File} file - Selected PDF file
 */
function handleFileSelect(file) {
    const topicInput = document.getElementById('topic-input');
    const fileDisplay = document.getElementById('file-display');
    const fileName = document.getElementById('file-name');

    if (topicInput && fileDisplay && fileName) {
        fileName.textContent = file.name;
        fileDisplay.style.display = 'flex';
        topicInput.disabled = true;
        topicInput.value = '';
    }
}

/**
 * Handles file removal
 */
function handleFileRemove() {
    const fileInput = document.getElementById('file-input');
    const topicInput = document.getElementById('topic-input');
    const fileDisplay = document.getElementById('file-display');

    if (fileInput && topicInput && fileDisplay) {
        fileInput.value = '';
        fileDisplay.style.display = 'none';
        topicInput.disabled = false;
        topicInput.focus();
    }
}
