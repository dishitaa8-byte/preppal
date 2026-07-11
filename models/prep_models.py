"""Data models for PrepPal application using dataclasses."""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Question:
    """Represents a single question generated for the session."""
    id: str
    text: str
    ideal_answer: str
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Answer:
    """Represents a user's answer to a question with evaluation."""
    id: str
    question_id: str
    user_answer: str
    evaluation: Optional[str] = None  # e.g., "Good", "Better", "Best"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PrepSession:
    """Represents a complete preparation session (topic or PDF based)."""
    id: str
    topic: Optional[str] = None
    pdf_filename: Optional[str] = None
    pdf_path: Optional[str] = None
    questions: List[Question] = field(default_factory=list)
    answers: List[Answer] = field(default_factory=list)
    current_question_index: int = 0
    is_complete: bool = False
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
