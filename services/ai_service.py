"""AI service for LLM interactions using NVIDIA API."""
from typing import List, Dict, Optional
import json
from openai import OpenAI
from services.prompt_service import PromptService


class AIService:
    """Service class for AI-related operations (LLM calls via NVIDIA API)."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: str = "meta/llama-3.1-405b-instruct"):
        """
        Initialize AI service.
        
        Args:
            api_key: NVIDIA API key
            base_url: Base URL for NVIDIA API
            model: Model to use for generation
        """
        self.api_key = api_key
        self.base_url = base_url or "https://integrate.api.nvidia.com/v1"
        self.model = model
        self.prompt_service = PromptService()
        
        # Initialize OpenAI client if we have API key
        self.client = None
        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
    
    def generate_questions(self, topic: Optional[str] = None, pdf_text: Optional[str] = None, num_questions: int = 5) -> List[Dict[str, str]]:
        """
        Generate viva questions based on topic or PDF text using NVIDIA API.
        
        Args:
            topic: Optional topic string
            pdf_text: Optional text extracted from PDF
            num_questions: Number of questions to generate
            
        Returns:
            List of dictionaries with 'question' and 'ideal_answer' keys
        """
        if not self.client:
            raise ValueError("NVIDIA API key not configured")
        
        # Get prompt
        system_prompt = self.prompt_service.get_examiner_system_prompt()
        user_prompt = self.prompt_service.get_question_generation_prompt(
            topic=topic,
            pdf_text=pdf_text,
            num_questions=num_questions
        )
        
        try:
            # Call NVIDIA API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4096
            )
            
            # Parse response
            response_text = response.choices[0].message.content.strip()
            # Try to extract JSON
            try:
                # Find JSON part (in case there's extra text)
                if "```json" in response_text:
                    json_str = response_text.split("```json")[1].split("```")[0].strip()
                elif "```" in response_text:
                    json_str = response_text.split("```")[1].strip()
                else:
                    json_str = response_text
                
                questions_data = json.loads(json_str)
                # Ensure it's a list
                if isinstance(questions_data, dict) and "questions" in questions_data:
                    questions_data = questions_data["questions"]
                elif not isinstance(questions_data, list):
                    raise ValueError("Invalid JSON format")
                
                # Validate each question has required fields
                valid_questions = []
                for q in questions_data:
                    if isinstance(q, dict) and "question" in q and "ideal_answer" in q:
                        valid_questions.append(q)
                    elif len(valid_questions) >= num_questions:
                        break
                
                return valid_questions[:num_questions]
            
            except json.JSONDecodeError:
                raise ValueError("Failed to parse AI response as JSON")
        
        except Exception as e:
            raise Exception(f"AI question generation failed: {str(e)}")
    
    def evaluate_answer(self, user_answer: str, ideal_answer: str) -> str:
        """
        Evaluate a user's answer using NVIDIA API.
        
        Args:
            user_answer: User's answer text
            ideal_answer: Ideal answer text
            
        Returns:
            Evaluation string (Good/Better/Best)
        """
        if not self.client:
            raise ValueError("NVIDIA API key not configured")
        
        system_prompt = self.prompt_service.get_examiner_system_prompt()
        user_prompt = self.prompt_service.get_answer_evaluation_prompt(user_answer, ideal_answer)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=64
            )
            
            result = response.choices[0].message.content.strip()
            # Normalize result
            if "Good" in result:
                return "Good"
            elif "Better" in result:
                return "Better"
            elif "Best" in result:
                return "Best"
            return "Good"  # Default
        
        except Exception as e:
            raise Exception(f"AI evaluation failed: {str(e)}")
    
    def generate_model_answer(self, question: str, context: Optional[str] = None) -> str:
        """
        Generate an ideal answer for a given question using NVIDIA API.
        
        Args:
            question: Question text
            context: Optional context (topic or PDF text)
            
        Returns:
            Generated ideal answer string
        """
        if not self.client:
            raise ValueError("NVIDIA API key not configured")
        
        system_prompt = self.prompt_service.get_examiner_system_prompt()
        user_prompt = self.prompt_service.get_ideal_answer_prompt(question, context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                max_tokens=2048
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise Exception(f"AI answer generation failed: {str(e)}")
