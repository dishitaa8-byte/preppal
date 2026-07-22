document.addEventListener('DOMContentLoaded', () => {
    const sessionId = SESSION_ID;
    
    const performanceMessage = document.getElementById('performance-message');
    const topicDisplay = document.getElementById('topic-display');
    const writtenStats = document.getElementById('written-stats');
    const mcqStats = document.getElementById('mcq-stats');
    const totalScore = document.getElementById('total-score');
    const maxScore = document.getElementById('max-score');
    const averageScore = document.getElementById('average-score');
    const questionsAttempted = document.getElementById('questions-attempted');
    const correctCount = document.getElementById('correct-count');
    const incorrectCount = document.getElementById('incorrect-count');
    const accuracyPercentage = document.getElementById('accuracy-percentage');
    const mcqQuestionsAttempted = document.getElementById('mcq-questions-attempted');
    const questionsReview = document.getElementById('questions-review');
    const newSessionBtn = document.getElementById('new-session-btn');
    const homeBtn = document.getElementById('home-btn');
    const loading = document.getElementById('loading');

    loadSummary();

    newSessionBtn.addEventListener('click', () => {
        window.location.href = '/';
    });

    homeBtn.addEventListener('click', () => {
        window.location.href = '/';
    });

    async function loadSummary() {
        showLoading(true, 'Loading summary...');
        try {
            const response = await fetch(`/api/session/${sessionId}/summary`);
            const data = await response.json();

            if (data.error) {
                alert(data.error);
                window.location.href = '/';
                return;
            }

            updateSummaryUI(data);
        } catch (error) {
            console.error('Error loading summary:', error);
            alert('Failed to load summary');
            window.location.href = '/';
        } finally {
            showLoading(false);
        }
    }

    function updateSummaryUI(data) {
        const mode = data.mode || 'written';
        
        // Update performance message and topic
        performanceMessage.textContent = data.performance_message;
        topicDisplay.textContent = `Topic: ${data.topic}`;

        // Show/hide appropriate stats based on mode
        if (mode === 'mcq') {
            writtenStats.style.display = 'none';
            mcqStats.style.display = 'grid';
            
            // Update MCQ stats
            correctCount.textContent = data.correct_count;
            incorrectCount.textContent = data.incorrect_count;
            accuracyPercentage.textContent = `${Math.round(data.accuracy_percentage)}%`;
            mcqQuestionsAttempted.textContent = `${data.questions_attempted}/${data.total_questions}`;
        } else {
            writtenStats.style.display = 'grid';
            mcqStats.style.display = 'none';
            
            // Update written stats with numerical scoring
            totalScore.textContent = `${data.total_score}`;
            maxScore.textContent = `${data.max_possible_score}`;
            averageScore.textContent = `${data.average_score.toFixed(1)}`;
            questionsAttempted.textContent = `${data.questions_attempted}/${data.total_questions}`;
        }

        // Build questions review
        questionsReview.innerHTML = '';
        data.questions_review.forEach((item, index) => {
            const questionCard = createQuestionCard(item, index, mode);
            questionsReview.appendChild(questionCard);
        });
    }

    function createQuestionCard(item, index, mode) {
        const card = document.createElement('div');
        card.className = 'geometric-card question-review-card';

        if (mode === 'mcq') {
            const badgeClass = item.is_correct === true ? 'correct' : (item.is_correct === false ? 'incorrect' : 'pending');
            const badgeText = item.is_correct === true ? 'Correct' : (item.is_correct === false ? 'Incorrect' : 'Not Answered');

            card.innerHTML = `
                <div class="review-header">
                    <span class="question-number">Question ${item.index}</span>
                    <span class="evaluation-badge ${badgeClass}">${badgeText}</span>
                </div>
                <div class="review-content">
                    <div class="review-section">
                        <h4 class="review-label">Question:</h4>
                        <p class="review-text">${item.question}</p>
                    </div>
                    <div class="review-section">
                        <h4 class="review-label">Options:</h4>
                        <div class="review-options">
                            ${(item.options || []).map((opt, i) => `
                                <div class="review-option ${opt === item.user_answer ? 'selected' : ''} ${opt === item.correct_answer ? 'correct' : ''}">
                                    ${opt}
                                    ${opt === item.user_answer ? '<span class="option-badge">Your Answer</span>' : ''}
                                    ${opt === item.correct_answer ? '<span class="option-badge correct-badge">Correct</span>' : ''}
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    <div class="review-section">
                        <h4 class="review-label">Your Answer:</h4>
                        <p class="review-text user-answer">${item.user_answer || 'Not answered'}</p>
                    </div>
                    <div class="review-section">
                        <h4 class="review-label">Correct Answer:</h4>
                        <p class="review-text ideal-answer">${item.correct_answer}</p>
                    </div>
                    <div class="review-section">
                        <h4 class="review-label">Explanation:</h4>
                        <p class="review-text">${item.explanation || 'No explanation provided'}</p>
                    </div>
                </div>
            `;
        } else {
            const scoreBadgeClass = item.score !== null ? 'score-badge' : 'pending';
            const scoreText = item.score !== null ? `${item.score}/5` : 'Not Answered';

            card.innerHTML = `
                <div class="review-header">
                    <span class="question-number">Question ${item.index}</span>
                    <span class="evaluation-badge ${scoreBadgeClass}">${scoreText}</span>
                </div>
                <div class="review-content">
                    <div class="review-section">
                        <h4 class="review-label">Question:</h4>
                        <p class="review-text">${item.question}</p>
                    </div>
                    <div class="review-section">
                        <h4 class="review-label">Your Answer:</h4>
                        <p class="review-text user-answer">${item.user_answer || 'Not answered'}</p>
                    </div>
                    <div class="review-section">
                        <h4 class="review-label">Score:</h4>
                        <p class="review-text score-text">${item.score !== null ? item.score : 'N/A'}</p>
                    </div>
                    <div class="review-section">
                        <h4 class="review-label">Feedback:</h4>
                        <p class="review-text feedback-text">${item.feedback || 'No feedback provided'}</p>
                    </div>
                    <div class="review-section">
                        <h4 class="review-label">Ideal Answer:</h4>
                        <p class="review-text ideal-answer">${item.ideal_answer}</p>
                    </div>
                </div>
            `;
        }

        return card;
    }

    function showLoading(show, text) {
        loading.style.display = show ? 'flex' : 'none';
        const loadingText = document.getElementById('loading-text');
        if (loadingText && text) {
            loadingText.textContent = text;
        }
    }
});
