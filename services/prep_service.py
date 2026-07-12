"""Prep service for orchestrating session start and question generation."""
import os
from typing import Optional, Tuple, Dict, Any
from werkzeug.datastructures import FileStorage
from models.prep_models import PrepSession
from utils.validators import validate_topic, validate_pdf_file


class PrepService:
    """Service class for preparation session workflows."""

    def __init__(self, session_service, ai_service, pdf_service):
        self.session_service = session_service
        self.ai_service = ai_service
        self.pdf_service = pdf_service

    def start_session(
        self,
        topic: str = "",
        pdf_file: Optional[FileStorage] = None,
        num_questions: int = 5
    ) -> Tuple[Optional[PrepSession], Optional[str]]:
        """
        Validate input and create a session without generating questions yet.

        Returns:
            Tuple of (PrepSession, error_message)
        """
        topic = topic.strip() if topic else ""
        pdf_text = None
        pdf_filename = None
        pdf_path = None

        if pdf_file and pdf_file.filename:
            is_valid, error = validate_pdf_file(pdf_file)
            if not is_valid:
                return None, error

            success, pdf_filename, error = self.pdf_service.save_pdf(pdf_file)
            if not success:
                return None, error

            success, pdf_text, error = self.pdf_service.extract_text(pdf_filename)
            if not success:
                return None, error

            pdf_path = os.path.join(self.pdf_service.upload_dir, pdf_filename)
        elif topic:
            is_valid, error = validate_topic(topic)
            if not is_valid:
                return None, error
        else:
            return None, "Please enter a topic or upload a PDF"

        prep_session = self.session_service.create_session(
            topic=topic if topic else None,
            pdf_filename=pdf_filename,
            pdf_path=pdf_path,
            num_questions=num_questions
        )
        prep_session.pdf_text = pdf_text

        return prep_session, None

    def generate_questions(self, session_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Generate questions for an existing session.

        Returns:
            Tuple of (result_dict, error_message)
        """
        prep_session = self.session_service.get_session(session_id)
        if not prep_session:
            return None, "Session not found"

        if prep_session.generation_status == "ready":
            return {
                "status": "success",
                "num_questions": len(prep_session.questions)
            }, None

        if prep_session.generation_status == "generating":
            return None, "Question generation already in progress"

        self.session_service.set_generation_status(session_id, "generating")

        try:
            num_questions = prep_session.num_questions
            questions_data = self.ai_service.generate_questions(
                topic=prep_session.topic,
                pdf_text=prep_session.pdf_text,
                num_questions=num_questions
            )

            for q_data in questions_data:
                self.session_service.add_question(
                    session_id=session_id,
                    question_text=q_data["question"],
                    ideal_answer=q_data["ideal_answer"]
                )

            self.session_service.set_generation_status(session_id, "ready")

            return {
                "status": "success",
                "num_questions": len(prep_session.questions)
            }, None

        except Exception as e:
            error_msg = f"Question generation failed: {str(e)}"
            self.session_service.set_generation_status(session_id, "failed", error_msg)
            return None, error_msg
