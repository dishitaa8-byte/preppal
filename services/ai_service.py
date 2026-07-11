"""AI service for LLM interactions (mock implementation for now)."""
from typing import List, Dict, Optional
import os
from utils.helpers import generate_unique_id


class AIService:
    """Service class for AI-related operations (LLM calls)."""
    
    def __init__(self, api_key: Optional[str] = None, provider: str = "openai"):
        """
        Initialize AI service.
        
        Args:
            api_key: API key for the LLM provider (read from config/env if not provided)
            provider: LLM provider name (openai, anthropic, etc.)
        """
        self.api_key = api_key or os.environ.get("AI_API_KEY")
        self.provider = provider
    
    def generate_questions(self, topic: Optional[str] = None, pdf_text: Optional[str] = None, num_questions: int = 5) -> List[Dict[str, str]]:
        """
        Generate viva questions based on topic or PDF text.
        
        Args:
            topic: Optional topic string
            pdf_text: Optional text extracted from PDF
            num_questions: Number of questions to generate
            
        Returns:
            List of dictionaries with 'question' and 'ideal_answer' keys
        """
        # TODO: Implement actual LLM call when ready
        # For now, return mock data
        mock_questions = [
            {
                "question": f"What is {topic or 'the topic'} about?",
                "ideal_answer": "This is a sample ideal answer that explains the concept clearly and comprehensively."
            },
            {
                "question": "Can you explain the key concepts in detail?",
                "ideal_answer": "The key concepts include [concept 1], [concept 2], and [concept 3], which are important because..."
            },
            {
                "question": "What are the practical applications of this topic?",
                "ideal_answer": "Practical applications include [application 1] in industry, [application 2] in research, and [application 3] in everyday life."
            },
            {
                "question": "What are the main challenges or limitations?",
                "ideal_answer": "Main challenges include [challenge 1], [challenge 2], and addressing these requires [solution approach]."
            },
            {
                "question": "How does this topic relate to real-world scenarios?",
                "ideal_answer": "This topic relates to real-world scenarios such as [scenario 1] and [scenario 2], where it is used to solve problems like [specific problem]."
            }
        ]
        return mock_questions[:num_questions]
    
    def evaluate_answer(self, user_answer: str, ideal_answer: str) -> str:
        """
        Evaluate a user's answer against the ideal answer.
        
        Args:
            user_answer: User's answer text
            ideal_answer: Ideal answer text
            
        Returns:
            Evaluation string (Good/Better/Best)
        """
        # TODO: Implement actual LLM call when ready
        # For now, return a mock evaluation randomly
        import random
        return random.choice(["Good", "Better", "Best"])
    
    def generate_model_answer(self, question: str) -> str:
        """
        Generate an ideal answer for a given question.
        
        Args:
            question: Question text
            
        Returns:
            Generated ideal answer string
        """
        # TODO: Implement actual LLM call when ready
        # For now, return a mock answer
        return f"This is a detailed ideal answer to the question: '{question}'. It covers all key points and provides a comprehensive explanation."
