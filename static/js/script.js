
document.addEventListener('DOMContentLoaded', () => {
    // Check if it's the user's first visit
    const isFirstVisit = localStorage.getItem('preppal_first_visit') === null;

    // Get DOM elements
    const welcomeText = document.getElementById('welcome-text');
    const tagline = document.getElementById('tagline');
    const divider = document.getElementById('divider');
    const actionSection = document.getElementById('action-section');

    if (isFirstVisit) {
        // First visit: play the intro animation
        playIntroAnimation(welcomeText, tagline, divider, actionSection);
        // Set flag in localStorage to not show intro again
        localStorage.setItem('preppal_first_visit', 'false');
    } else {
        // Returning visit: show everything immediately
        showAllElements(welcomeText, tagline, divider, actionSection);
    }

    // Upload card click handler (placeholder for future functionality)
    const uploadCard = document.getElementById('upload-card');
    if (uploadCard) {
        uploadCard.addEventListener('click', () => {
            console.log('Upload card clicked - file upload will be added later');
        });
    }

    // Start prep button click handler (placeholder for future functionality)
    const startBtn = document.getElementById('start-btn');
    if (startBtn) {
        startBtn.addEventListener('click', () => {
            console.log('Start Prep button clicked - question generation will be added later');
        });
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
