document.addEventListener('DOMContentLoaded', () => {
    const sessionId = SESSION_ID;
    let currentQuestionData = null;

    const questionText = document.getElementById('question-text');
    const answerInput = document.getElementById('answer-input');
    const submitBtn = document.getElementById('submit-btn');
    const progressText = document.getElementById('progress-text');
    const progressFill = document.getElementById('progress-fill');
    const charCounter = document.getElementById('char-counter');
    const submittedNotice = document.getElementById('submitted-notice');
    const loading = document.getElementById('loading');
    const loadingText = document.getElementById('loading-text');

    loadQuestion();

    submitBtn.addEventListener('click', submitAnswer);
    answerInput.addEventListener('input', updateCharCounter);

    async function loadQuestion() {
        showLoading(true, 'Loading question...');
        try {
            const response = await fetch(`/api/session/${sessionId}/question`);
            const data = await response.json();

            if (data.error) {
                alert(data.error);
                if (data.error === 'Questions not ready yet') {
                    window.location.href = `/prep/${sessionId}/loading`;
                }
                return;
            }

            currentQuestionData = data.question;
            updateUI(data.question);
        } catch (error) {
            console.error('Error loading question:', error);
            alert('Failed to load question');
        } finally {
            showLoading(false);
        }
    }

    async function submitAnswer() {
        const answer = answerInput.value.trim();
        if (!answer) {
            alert('Please enter an answer');
            return;
        }

        submitBtn.disabled = true;
        showLoading(true, 'Evaluating your answer...');

        try {
            const response = await fetch(`/api/session/${sessionId}/answer`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ answer })
            });

            const data = await response.json();

            if (data.error) {
                alert(data.error);
                submitBtn.disabled = false;
                return;
            }

            showSubmittedState();
        } catch (error) {
            console.error('Error submitting answer:', error);
            alert('Failed to submit answer');
            submitBtn.disabled = false;
        } finally {
            showLoading(false);
        }
    }

    function updateUI(question) {
        questionText.textContent = question.text;
        answerInput.value = '';
        answerInput.disabled = false;
        submitBtn.disabled = false;
        progressText.textContent = `Question ${question.index + 1} of ${question.total}`;

        const progressPercent = ((question.index + 1) / question.total) * 100;
        progressFill.style.width = `${progressPercent}%`;

        updateCharCounter();
        submittedNotice.style.display = 'none';
        submitBtn.style.display = 'block';
    }

    function updateCharCounter() {
        const count = answerInput.value.length;
        charCounter.textContent = `${count} character${count === 1 ? '' : 's'}`;
    }

    function showSubmittedState() {
        answerInput.disabled = true;
        submitBtn.style.display = 'none';
        submittedNotice.style.display = 'block';
    }

    function showLoading(show, text) {
        loading.style.display = show ? 'flex' : 'none';
        if (text && loadingText) {
            loadingText.textContent = text;
        }
    }
});
