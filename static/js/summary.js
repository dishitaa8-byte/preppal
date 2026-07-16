document.addEventListener('DOMContentLoaded', () => {
    const sessionId = SESSION_ID;
    
    const performanceMessage = document.getElementById('performance-message');
    const topicDisplay = document.getElementById('topic-display');
    const questionsAttempted = document.getElementById('questions-attempted');
    const completionPercentage = document.getElementById('completion-percentage');
    const bestCount = document.getElementById('best-count');
    const betterCount = document.getElementById('better-count');
    const goodCount = document.getElementById('good-count');
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
        // Update performance message and topic
        performanceMessage.textContent = data.performance_message;
        topicDisplay.textContent = `Topic: ${data.topic}`;

        // Update stats
        questionsAttempted.textContent = `${data.questions_attempted}/${data.total_questions}`;
        completionPercentage.textContent = `${Math.round(data.completion_percentage)}%`;

        // Update evaluation counts
        bestCount.textContent = data.best_count;
        betterCount.textContent = data.better_count;
        goodCount.textContent = data.good_count;

        // Build questions review
        questionsReview.innerHTML = '';
        data.questions_review.forEach((item, index) => {
            const questionCard = createQuestionCard(item, index);
            questionsReview.appendChild(questionCard);
        });
    }

    function createQuestionCard(item, index) {
        const card = document.createElement('div');
        card.className = 'geometric-card question-review-card';

        const badgeClass = item.evaluation ? item.evaluation.toLowerCase() : 'pending';
        const badgeText = item.evaluation || 'Not Answered';

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
                    <h4 class="review-label">Your Answer:</h4>
                    <p class="review-text user-answer">${item.user_answer || 'Not answered'}</p>
                </div>
                <div class="review-section">
                    <h4 class="review-label">Ideal Answer:</h4>
                    <p class="review-text ideal-answer">${item.ideal_answer}</p>
                </div>
            </div>
        `;

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
