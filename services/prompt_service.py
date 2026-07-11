"""Prompt service for generating LLM prompts."""
from typing import Optional


class PromptService:
    """Service class for generating prompts for LLM operations."""
    
    def get_question_generation_prompt(self, topic: Optional[str] = None, pdf_text: Optional[str] = None, num_questions: int = 5) -> str:
        """
        Generate a prompt for question generation.
        
        Args:
            topic: Optional topic string
            pdf_text: Optional text extracted from PDF
            num_questions: Number of questions to generate
            
        Returns:
            Formatted prompt string
        """
        context = ""
        if topic:
            context = f"Topic: {topic}"
        elif pdf_text:
            context = f"Content from PDF:\n{pdf_text[:4000]}..."  # Truncate to avoid token limits
        
        return f"""You are an expert educator preparing viva questions.
{context}

Please generate {num_questions} viva-style questions that test deep understanding of the material.
For each question, also provide an ideal answer.

Return your response in JSON format with a list of objects, each with "question" and "ideal_answer" keys."""
    
    def get_answer_evaluation_prompt(self, user_answer: str, ideal_answer: str) -> str:
        """
        Generate a prompt for answer evaluation.
        
        Args:
            user_answer: User's answer text
            ideal_answer: Ideal answer text
            
        Returns:
            Formatted prompt string
        """
        return f"""You are an expert educator evaluating student answers.

User Answer: {user_answer}
Ideal Answer: {ideal_answer}

Please evaluate the user's answer and classify it as one of:
- "Good": Covers most key points correctly
- "Better": Covers all key points with good explanation
- "Best": Excellent explanation that exceeds expectations

Return only the classification string (Good/Better/Best)."""
    
    def get_ideal_answer_prompt(self, question: str, context: Optional[str] = None) -> str:
        """
        Generate a prompt for ideal answer generation.
        
        Args:
            question: Question text
            context: Optional context (topic or PDF text)
            
        Returns:
            Formatted prompt string
        """
        context_part = f"\nContext: {context}" if context else ""
        
        return f"""You are an expert educator.

Question: {question}{context_part}

Please provide a comprehensive, clear, and accurate ideal answer to this question that covers all key points."""
