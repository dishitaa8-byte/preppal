document.addEventListener('DOMContentLoaded', () => {
    const sessionId = SESSION_ID;
    let currentQuestionData = null;
    let currentMode = 'written';
    let selectedMCQOption = null;

    const questionText = document.getElementById('question-text');
    const answerInput = document.getElementById('answer-input');
    const answerCard = document.getElementById('answer-card');
    const mcqCard = document.getElementById('mcq-card');
    const mcqOptions = document.getElementById('mcq-options');
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
            currentMode = data.mode || 'written';
            updateUI(data.question, currentMode);
        } catch (error) {
            console.error('Error loading question:', error);
            alert('Failed to load question');
        } finally {
            showLoading(false);
        }
    }

    async function submitAnswer() {
        let answer = '';
        
        if (currentMode === 'mcq') {
            answer = selectedMCQOption;
            if (!answer) {
                alert('Please select an option');
                return;
            }
        } else {
            answer = answerInput.value.trim();
            if (!answer) {
                alert('Please enter an answer');
                return;
            }
        }

        submitBtn.disabled = true;
        showLoading(true, 'Submitting your answer...');

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

            // Move to next question
            const nextResponse = await fetch(`/api/session/${sessionId}/next`, {
                method: 'POST'
            });
            const nextData = await nextResponse.json();

            if (nextData.error) {
                alert(nextData.error);
                submitBtn.disabled = false;
                return;
            }

            if (nextData.is_complete) {
                window.location.href = `/prep/${sessionId}/summary`;
            } else {
                loadQuestion();
            }
        } catch (error) {
            console.error('Error submitting answer:', error);
            alert('Failed to submit answer');
            submitBtn.disabled = false;
        } finally {
            showLoading(false);
        }
    }

    function updateUI(question, mode) {
        questionText.textContent = question.text;
        selectedMCQOption = null;
        
        // Show/hide appropriate UI based on mode
        if (mode === 'mcq') {
            answerCard.style.display = 'none';
            mcqCard.style.display = 'block';
            renderMCQOptions(question.options || []);
        } else {
            answerCard.style.display = 'block';
            mcqCard.style.display = 'none';
            answerInput.value = '';
            answerInput.disabled = false;
            updateCharCounter();
        }
        
        submitBtn.disabled = false;
        progressText.textContent = `Question ${question.index + 1} of ${question.total}`;

        const progressPercent = ((question.index + 1) / question.total) * 100;
        progressFill.style.width = `${progressPercent}%`;

        submittedNotice.style.display = 'none';
        submitBtn.style.display = 'block';
    }

    function renderMCQOptions(options) {
        mcqOptions.innerHTML = '';
        
        options.forEach((option, index) => {
            const optionElement = document.createElement('div');
            optionElement.className = 'mcq-option';
            optionElement.innerHTML = `
                <input type="radio" name="mcq-option" value="${option}" id="option-${index}">
                <span class="mcq-radio"></span>
                <span class="mcq-option-text">${option}</span>
            `;
            
            optionElement.addEventListener('click', () => {
                // Remove selected class from all options
                document.querySelectorAll('.mcq-option').forEach(opt => {
                    opt.classList.remove('selected');
                });
                // Add selected class to clicked option
                optionElement.classList.add('selected');
                selectedMCQOption = option;
            });
            
            mcqOptions.appendChild(optionElement);
        });
    }

    function updateCharCounter() {
        const count = answerInput.value.length;
        charCounter.textContent = `${count} character${count === 1 ? '' : 's'}`;
    }

    function showSubmittedState() {
        if (currentMode === 'mcq') {
            document.querySelectorAll('.mcq-option').forEach(opt => {
                opt.style.pointerEvents = 'none';
            });
        } else {
            answerInput.disabled = true;
        }
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
