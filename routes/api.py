"""API routes for PrepPal application."""
from flask import Blueprint, request, jsonify, current_app

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/start", methods=["POST"])
def start_session():
    """Create a new preparation session (topic or PDF). Questions are generated separately."""
    try:
        topic = request.form.get("topic", "").strip()
        pdf_file = request.files.get("pdf") if "pdf" in request.files else None

        prep_session, error = current_app.prep_service.start_session(
            topic=topic,
            pdf_file=pdf_file
        )

        if error:
            return jsonify({"error": error}), 400

        return jsonify({
            "status": "success",
            "session_id": prep_session.id
        }), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Session start failed: {str(e)}"}), 500


@api_bp.route("/session/<session_id>/generate", methods=["POST"])
def generate_questions(session_id: str):
    """Generate questions for an existing session."""
    try:
        result, error = current_app.prep_service.generate_questions(session_id)

        if error:
            status_code = 404 if error == "Session not found" else 500
            return jsonify({"error": error}), status_code

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Question generation failed: {str(e)}"}), 500


@api_bp.route("/session/<session_id>/status", methods=["GET"])
def get_session_status(session_id: str):
    """Get generation status for a session."""
    try:
        prep_session = current_app.session_service.get_session(session_id)
        if not prep_session:
            return jsonify({"error": "Session not found"}), 404

        return jsonify({
            "generation_status": prep_session.generation_status,
            "num_questions": len(prep_session.questions),
            "generation_error": prep_session.generation_error
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get session status: {str(e)}"}), 500


@api_bp.route("/session/<session_id>/question", methods=["GET"])
def get_current_question(session_id: str):
    """Get the current question for a session."""
    try:
        prep_session = current_app.session_service.get_session(session_id)
        if not prep_session:
            return jsonify({"error": "Session not found"}), 404

        if not current_app.session_service.is_questions_ready(session_id):
            return jsonify({"error": "Questions not ready yet"}), 400

        question = current_app.session_service.get_current_question(session_id)
        if not question:
            return jsonify({"error": "No more questions"}), 404

        return jsonify({
            "question": {
                "id": question.id,
                "text": question.text,
                "index": prep_session.current_question_index,
                "total": len(prep_session.questions)
            },
            "is_complete": prep_session.is_complete
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get question: {str(e)}"}), 500


@api_bp.route("/session/<session_id>/answer", methods=["POST"])
def submit_answer(session_id: str):
    """Submit an answer for evaluation."""
    try:
        data = request.get_json() or {}
        user_answer = data.get("answer", "").strip()

        if not user_answer:
            return jsonify({"error": "Please provide an answer"}), 400

        prep_session = current_app.session_service.get_session(session_id)
        if not prep_session:
            return jsonify({"error": "Session not found"}), 404

        question = current_app.session_service.get_current_question(session_id)
        if not question:
            return jsonify({"error": "No active question"}), 400

        answer = current_app.session_service.add_answer(
            session_id=session_id,
            question_id=question.id,
            user_answer=user_answer
        )

        rating = current_app.evaluation_service.evaluate_answer(
            question=question.text,
            user_answer=user_answer,
            ideal_answer=question.ideal_answer
        )
        current_app.session_service.update_answer_evaluation(session_id, answer.id, rating)

        return jsonify({
            "status": "success",
            "answer_id": answer.id
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to submit answer: {str(e)}"}), 500


@api_bp.route("/session/<session_id>/next", methods=["POST"])
def next_question(session_id: str):
    """Move to the next question in the session."""
    try:
        prep_session = current_app.session_service.get_session(session_id)
        if not prep_session:
            return jsonify({"error": "Session not found"}), 404

        current_app.session_service.next_question(session_id)
        is_complete = prep_session.is_complete

        return jsonify({
            "status": "success",
            "is_complete": is_complete
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to move to next question: {str(e)}"}), 500
