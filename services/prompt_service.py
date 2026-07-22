"""Prompt service for generating LLM prompts with examiner persona."""
from typing import Optional


class PromptService:
    """Service class for generating prompts for LLM operations."""
    
    def get_examiner_system_prompt(self) -> str:
        """
        Get system prompt defining the examiner persona.
        
        Returns:
            System prompt string
        """
        return """You are an experienced university examiner with 20+ years of conducting viva voce examinations. You specialize in creating high-quality, thought-provoking questions that test deep understanding rather than memorization.

Your responsibilities:
1. Create questions that gradually increase in difficulty
2. Ensure questions cover key concepts without repetition
3. Provide concise, accurate ideal answers
4. Always return structured, valid JSON"""
    
    def get_question_generation_prompt(self, topic: Optional[str] = None, pdf_text: Optional[str] = None, num_questions: int = 5, mode: str = "written") -> str:
        """
        Generate a prompt for question generation with clear JSON schema.
        
        Args:
            topic: Optional topic string
            pdf_text: Optional text extracted from PDF
            num_questions: Number of questions to generate
            mode: "written" for descriptive questions or "mcq" for multiple choice
            
        Returns:
            Formatted prompt string
        """
        context = ""
        if topic:
            context = f"TOPIC:\n{topic}"
        elif pdf_text:
            # Truncate to avoid token limits (keep ~3500 chars)
            truncated_text = pdf_text[:3500] + ("..." if len(pdf_text) > 3500 else "")
            context = f"CONTENT FROM PDF:\n{truncated_text}"
        
        if mode == "mcq":
            return f"""{context}

INSTRUCTIONS:
Generate exactly {num_questions} multiple-choice questions following these rules:
1. Questions should test understanding of key concepts
2. Each question must have exactly 4 options (A, B, C, D)
3. Only one option is correct
4. Options should be plausible but clearly distinguishable
5. Provide a brief explanation for the correct answer
6. Questions should gradually increase in difficulty
7. No repeating questions or concepts
8. Base all questions ONLY on the provided context above

RESPONSE FORMAT (JSON):
{{
  "questions": [
    {{
      "question": "Your question here",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "correct_answer": "The correct option text",
      "explanation": "Brief explanation of why this is correct"
    }}
  ]
}}

Return ONLY valid JSON, no other text."""
        else:
            return f"""{context}

INSTRUCTIONS:
Generate {num_questions} viva examination questions following these rules:
1. Questions should be 1-2 marks each (short answer, not multiple choice)
2. Questions should gradually increase in difficulty
3. No repeating questions or concepts
4. Each question must have a clear, concise ideal answer
5. Base all questions ONLY on the provided context above

RESPONSE FORMAT (JSON):
{{
  "questions": [
    {{
      "question": "Your question here",
      "ideal_answer": "The ideal answer here"
    }}
  ]
}}

Return ONLY valid JSON, no other text."""
    
    def get_answer_evaluation_prompt(self, user_answer: str, ideal_answer: str) -> str:
        """
        Generate a prompt for answer evaluation.
        
        Args:
            user_answer: User's answer text
            ideal_answer: Ideal answer text
            
        Returns:
            Formatted prompt string
        """
        return f"""USER ANSWER: {user_answer}
IDEAL ANSWER: {ideal_answer}

EVALUATION CRITERIA:
Evaluate the user's answer on a scale of 0 to 5:
- 0: Completely incorrect or no answer
- 1: Minimal understanding, mostly incorrect
- 2: Basic understanding but missing key points
- 3: Good understanding, covers most key points
- 4: Very good understanding, covers all key points well
- 5: Excellent understanding, exceeds expectations with detailed explanation

Provide:
1. A score (integer 0-5)
2. Concise feedback (2-4 sentences) explaining the score
3. The ideal answer (as provided above)

RESPONSE FORMAT (JSON):
{{
  "score": 4,
  "feedback": "Your feedback here...",
  "ideal_answer": "{ideal_answer}"
}}

Return ONLY valid JSON, no other text."""
    
    def get_ideal_answer_prompt(self, question: str, context: Optional[str] = None) -> str:
        """
        Generate a prompt for ideal answer generation.
        
        Args:
            question: Question text
            context: Optional context (topic or PDF text)
            
        Returns:
            Formatted prompt string
        """
        context_part = f"\nCONTEXT:\n{context[:2000]}" if context else ""
        
        return f"""QUESTION: {question}{context_part}

INSTRUCTIONS: Provide a comprehensive, clear, and accurate ideal answer to this question that covers all key points concisely."""
