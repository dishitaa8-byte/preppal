document.addEventListener('DOMContentLoaded', () => {
    const sessionId = SESSION_ID;

    const MESSAGES = [
        'Reporting to Hero Training Center...',
        'Preparing your next challenge...',
        'Generating Questions...'
    ];

    const messageEl = document.getElementById('loading-message');
    let messageIndex = 0;
    let messageInterval = null;

    startMessageCycle();
    generateQuestions();

    function startMessageCycle() {
        showMessage(0);

        messageInterval = setInterval(() => {
            fadeOutMessage(() => {
                messageIndex = (messageIndex + 1) % MESSAGES.length;
                showMessage(messageIndex);
            });
        }, 2500);
    }

    function showMessage(index) {
        if (!messageEl) return;
        messageEl.textContent = MESSAGES[index];
        messageEl.classList.remove('fade-out');
        messageEl.classList.add('fade-in');
    }

    function fadeOutMessage(callback) {
        if (!messageEl) {
            callback();
            return;
        }
        messageEl.classList.remove('fade-in');
        messageEl.classList.add('fade-out');
        setTimeout(callback, 500);
    }

    async function generateQuestions() {
        try {
            const response = await fetch(`/api/session/${sessionId}/generate`, {
                method: 'POST'
            });
            const data = await response.json();

            if (data.error) {
                clearInterval(messageInterval);
                alert(data.error);
                window.location.href = '/';
                return;
            }

            clearInterval(messageInterval);
            fadeOutMessage(() => {
                window.location.href = `/prep/${sessionId}`;
            });
        } catch (error) {
            console.error('Error generating questions:', error);
            clearInterval(messageInterval);
            alert('Failed to generate questions. Please try again.');
            window.location.href = '/';
        }
    }
});
