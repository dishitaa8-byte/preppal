"""API routes for PrepPal application."""
from flask import Blueprint, request, jsonify

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/start", methods=["POST"])
def start_session():
    """Start a new preparation session (topic or PDF)."""
    # TODO: Implement session start
    return jsonify({"status": "success", "session_id": "mock_session_id"}), 200


@api_bp.route("/session/<session_id>/question", methods=["GET"])
def get_current_question(session_id: str):
    """Get the current question for a session."""
    # TODO: Implement question retrieval
    return jsonify({"question": "Mock question text"}), 200


@api_bp.route("/session/<session_id>/answer", methods=["POST"])
def submit_answer(session_id: str):
    """Submit an answer for a question."""
    # TODO: Implement answer submission
    return jsonify({"status": "success"}), 200


@api_bp.route("/session/<session_id>/next", methods=["POST"])
def next_question(session_id: str):
    """Move to the next question in the session."""
    # TODO: Implement next question
    return jsonify({"status": "success"}), 200
