"""Evaluation service for handling answer evaluations (placeholder)."""


class EvaluationService:
    """Service class for answer evaluation operations."""
    
    def __init__(self, ai_service):
        """
        Initialize evaluation service with AI service.
        
        Args:
            ai_service: Instance of AIService for LLM interactions
        """
        self.ai_service = ai_service
    
    def evaluate_answer(
        self,
        question: str,
        user_answer: str,
        ideal_answer: str
    ) -> str:
        """
        Evaluate a user's answer using AI.

        Args:
            question: The question text
            user_answer: User's answer text
            ideal_answer: Ideal answer text

        Returns:
            Evaluation string (Good/Better/Best)
        """
        return self.ai_service.evaluate_answer(user_answer, ideal_answer)
    
    def get_detailed_feedback(self, user_answer: str, ideal_answer: str) -> str:
        """
        Get detailed feedback on a user's answer.
        
        Args:
            user_answer: User's answer text
            ideal_answer: Ideal answer text
            
        Returns:
            Detailed feedback string
        """
        # TODO: Implement detailed feedback generation
        return "Detailed feedback will be available in a future version."
