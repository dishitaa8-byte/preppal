document.addEventListener('DOMContentLoaded', () => {
    const sessionId = SESSION_ID;
    let currentQuestionData = null;
    
    // DOM Elements
    const questionText = document.getElementById('question-text');
    const answerInput = document.getElementById('answer-input');
    const submitBtn = document.getElementById('submit-btn');
    const progressText = document.getElementById('progress-text');
    const progressFill = document.getElementById('progress-fill');
    const resultSection = document.getElementById('result-section');
    const ratingDisplay = document.getElementById('rating-display');
    const idealAnswerText = document.getElementById('ideal-answer-text');
    const nextBtn = document.getElementById('next-btn');
    const completeSection = document.getElementById('complete-section');
    const loading = document.getElementById('loading');
    
    // Initialize
    loadQuestion();
    
    // Event listeners
    submitBtn.addEventListener('click', submitAnswer);
    nextBtn.addEventListener('click', goToNextQuestion);
    
    async function loadQuestion() {
        showLoading(true);
        try {
            const response = await fetch(`/api/session/${sessionId}/question`);
            const data = await response.json();
            
            if (data.error) {
                alert(data.error);
                return;
            }
            
            if (data.is_complete) {
                showComplete();
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
        
        showLoading(true);
        try {
            const response = await fetch(`/api/session/${sessionId}/answer`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ answer })
            });
            
            const data = await response.json();
            
            if (data.error) {
                alert(data.error);
                return;
            }
            
            showResult(data);
        } catch (error) {
            console.error('Error submitting answer:', error);
            alert('Failed to submit answer');
        } finally {
            showLoading(false);
        }
    }
    
    async function goToNextQuestion() {
        showLoading(true);
        try {
            const response = await fetch(`/api/session/${sessionId}/next`, {
                method: 'POST'
            });
            const data = await response.json();
            
            if (data.error) {
                alert(data.error);
                return;
            }
            
            if (data.is_complete) {
                showComplete();
                return;
            }
            
            // Reset UI and load next question
            resetForNextQuestion();
            loadQuestion();
        } catch (error) {
            console.error('Error moving to next question:', error);
            alert('Failed to load next question');
        } finally {
            showLoading(false);
        }
    }
    
    function updateUI(question) {
        questionText.textContent = question.text;
        answerInput.value = '';
        answerInput.disabled = false;
        progressText.textContent = `Question ${question.index + 1} of ${question.total}`;
        
        // Update progress bar
        const progressPercent = ((question.index + 1) / question.total) * 100;
        progressFill.style.width = `${progressPercent}%`;
        
        // Show/hide sections
        document.getElementById('question-card').style.display = 'block';
        document.getElementById('answer-card').style.display = 'block';
        submitBtn.style.display = 'block';
        resultSection.style.display = 'none';
        completeSection.style.display = 'none';
    }
    
    function showResult(data) {
        // Disable input and submit button
        answerInput.disabled = true;
        submitBtn.style.display = 'none';
        
        // Show result section
        resultSection.style.display = 'block';
        ratingDisplay.textContent = data.rating;
        ratingDisplay.className = 'rating-display';
        ratingDisplay.classList.add(data.rating.toLowerCase());
        idealAnswerText.textContent = data.ideal_answer;
    }
    
    function resetForNextQuestion() {
        answerInput.value = '';
        resultSection.style.display = 'none';
    }
    
    function showComplete() {
        document.getElementById('question-card').style.display = 'none';
        document.getElementById('answer-card').style.display = 'none';
        submitBtn.style.display = 'none';
        resultSection.style.display = 'none';
        completeSection.style.display = 'block';
    }
    
    function showLoading(show) {
        loading.style.display = show ? 'flex' : 'none';
    }
});
