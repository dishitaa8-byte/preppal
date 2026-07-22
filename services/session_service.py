"""Session service for managing PrepPal preparation sessions."""
from typing import Optional, Dict
from models.prep_models import PrepSession, Question, Answer
from utils.helpers import generate_unique_id


class SessionService:
    """Service class for managing preparation sessions."""
    
    def __init__(self):
        """Initialize session service with in-memory storage (for now)."""
        # In a real app, this would be a database
        self.sessions: Dict[str, PrepSession] = {}
    
    def create_session(
        self,
        topic: Optional[str] = None,
        pdf_filename: Optional[str] = None,
        pdf_path: Optional[str] = None,
        num_questions: int = 5,
        mode: str = "written"
    ) -> PrepSession:
        """
        Create a new preparation session.
        
        Args:
            topic: Optional topic for text-based session
            pdf_filename: Optional filename of uploaded PDF
            pdf_path: Optional path to uploaded PDF
            num_questions: Number of questions to generate
            mode: "written" or "mcq"
            
        Returns:
            Newly created PrepSession object
        """
        session_id = generate_unique_id()
        session = PrepSession(
            id=session_id,
            topic=topic,
            pdf_filename=pdf_filename,
            pdf_path=pdf_path,
            num_questions=num_questions,
            mode=mode
        )
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[PrepSession]:
        """
        Get a session by ID.
        
        Args:
            session_id: ID of the session to retrieve
            
        Returns:
            PrepSession object if found, None otherwise
        """
        return self.sessions.get(session_id)
    
    def add_question(self, session_id: str, question_text: str, ideal_answer: str, options: Optional[list] = None, correct_answer: Optional[str] = None, explanation: Optional[str] = None) -> Optional[Question]:
        """
        Add a question to a session.
        
        Args:
            session_id: ID of the session
            question_text: Text of the question
            ideal_answer: Ideal answer for the question
            options: List of options for MCQ mode
            correct_answer: Correct answer for MCQ mode
            explanation: Explanation for MCQ mode
            
        Returns:
            Created Question object if session found, None otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        question_id = generate_unique_id()
        question = Question(
            id=question_id,
            text=question_text,
            ideal_answer=ideal_answer,
            options=options,
            correct_answer=correct_answer,
            explanation=explanation
        )
        session.questions.append(question)
        return question
    
    def add_answer(self, session_id: str, question_id: str, user_answer: str) -> Optional[Answer]:
        """
        Add a user's answer to a session.
        
        Args:
            session_id: ID of the session
            question_id: ID of the question being answered
            user_answer: User's answer text
            
        Returns:
            Created Answer object if session found, None otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        answer_id = generate_unique_id()
        answer = Answer(
            id=answer_id,
            question_id=question_id,
            user_answer=user_answer
        )
        session.answers.append(answer)
        return answer
    
    def update_answer_score_feedback(self, session_id: str, answer_id: str, score: int, feedback: str) -> Optional[Answer]:
        """
        Update score and feedback of an answer for written mode.
        
        Args:
            session_id: ID of the session
            answer_id: ID of the answer
            score: Score (0-5)
            feedback: AI feedback text
            
        Returns:
            Updated Answer object if found, None otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        for answer in session.answers:
            if answer.id == answer_id:
                answer.score = score
                answer.feedback = feedback
                return answer
        return None

    def update_answer_correctness(self, session_id: str, answer_id: str, is_correct: bool) -> Optional[Answer]:
        """
        Update correctness of an answer for MCQ mode.
        
        Args:
            session_id: ID of the session
            answer_id: ID of the answer
            is_correct: Whether the answer is correct
            
        Returns:
            Updated Answer object if found, None otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        for answer in session.answers:
            if answer.id == answer_id:
                answer.is_correct = is_correct
                return answer
        return None
    
    def get_current_question(self, session_id: str) -> Optional[Question]:
        """
        Get the current question in a session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            Current Question object, None if no questions or session complete
        """
        session = self.get_session(session_id)
        if not session or session.is_complete:
            return None
        
        if 0 <= session.current_question_index < len(session.questions):
            return session.questions[session.current_question_index]
        return None
    
    def next_question(self, session_id: str) -> Optional[Question]:
        """
        Move to the next question in a session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            Next Question object if available, None if end of questions
        """
        session = self.get_session(session_id)
        if not session or session.is_complete:
            return None
        
        session.current_question_index += 1
        
        if session.current_question_index >= len(session.questions):
            session.is_complete = True
            return None
        
        return self.get_current_question(session_id)

    def set_generation_status(
        self,
        session_id: str,
        status: str,
        error: Optional[str] = None
    ) -> Optional[PrepSession]:
        """Update question generation status for a session."""
        session = self.get_session(session_id)
        if not session:
            return None
        session.generation_status = status
        session.generation_error = error
        return session

    def is_questions_ready(self, session_id: str) -> bool:
        """Check whether questions have been generated for a session."""
        session = self.get_session(session_id)
        return session is not None and session.generation_status == "ready"
