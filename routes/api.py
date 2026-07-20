"""API routes for PrepPal application."""
from flask import Blueprint, request, jsonify, current_app

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/start", methods=["POST"])
def start_session():
    """Create a new preparation session (topic or PDF). Questions are generated separately."""
    try:
        topic = request.form.get("topic", "").strip()
        pdf_file = request.files.get("pdf") if "pdf" in request.files else None
        mode = request.form.get("mode", "written")

        # Set num_questions based on mode
        num_questions = 10 if mode == "mcq" else 5

        prep_session, error = current_app.prep_service.start_session(
            topic=topic,
            pdf_file=pdf_file,
            num_questions=num_questions,
            mode=mode
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

        question_data = {
            "id": question.id,
            "text": question.text,
            "index": prep_session.current_question_index,
            "total": len(prep_session.questions)
        }

        # Add MCQ-specific data if in MCQ mode
        if prep_session.mode == "mcq" and question.options:
            question_data["options"] = question.options

        return jsonify({
            "question": question_data,
            "mode": prep_session.mode,
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

        # Handle evaluation based on mode
        if prep_session.mode == "mcq":
            # For MCQ, compare with correct answer
            is_correct = (user_answer == question.correct_answer)
            current_app.session_service.update_answer_correctness(session_id, answer.id, is_correct)
        else:
            # For written mode, use AI evaluation
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


@api_bp.route("/session/<session_id>/summary", methods=["GET"])
def get_session_summary(session_id: str):
    """Get summary data for a completed session."""
    try:
        prep_session = current_app.session_service.get_session(session_id)
        if not prep_session:
            return jsonify({"error": "Session not found"}), 404

        mode = prep_session.mode
        total_questions = len(prep_session.questions)
        answered_questions = len(prep_session.answers)
        completion_percentage = (answered_questions / total_questions * 100) if total_questions > 0 else 0

        if mode == "mcq":
            # MCQ mode summary
            correct_count = 0
            incorrect_count = 0
            
            for answer in prep_session.answers:
                if answer.is_correct:
                    correct_count += 1
                else:
                    incorrect_count += 1
            
            # Generate performance message based on accuracy
            accuracy = (correct_count / answered_questions * 100) if answered_questions > 0 else 0
            if accuracy >= 90:
                performance_message = "Outstanding Hero!"
            elif accuracy >= 75:
                performance_message = "Excellent Work!"
            elif accuracy >= 60:
                performance_message = "Keep Training!"
            else:
                performance_message = "Needs More Practice!"
            
            # Build question review data for MCQ
            questions_review = []
            for i, question in enumerate(prep_session.questions):
                user_answer = None
                is_correct = None
                for answer in prep_session.answers:
                    if answer.question_id == question.id:
                        user_answer = answer.user_answer
                        is_correct = answer.is_correct
                        break
                
                questions_review.append({
                    "index": i + 1,
                    "question": question.text,
                    "options": question.options,
                    "user_answer": user_answer,
                    "correct_answer": question.correct_answer,
                    "is_correct": is_correct,
                    "explanation": question.explanation
                })

            return jsonify({
                "mode": mode,
                "topic": prep_session.topic or "PDF-based session",
                "questions_attempted": answered_questions,
                "total_questions": total_questions,
                "correct_count": correct_count,
                "incorrect_count": incorrect_count,
                "accuracy_percentage": accuracy,
                "performance_message": performance_message,
                "questions_review": questions_review
            }), 200
        else:
            # Written mode summary (existing logic)
            good_count = 0
            better_count = 0
            best_count = 0
            
            for answer in prep_session.answers:
                if answer.evaluation == "Good":
                    good_count += 1
                elif answer.evaluation == "Better":
                    better_count += 1
                elif answer.evaluation == "Best":
                    best_count += 1
            
            # Generate overall performance message
            if best_count >= answered_questions * 0.8:
                performance_message = "Excellent work."
            elif best_count + better_count >= answered_questions * 0.7:
                performance_message = "Great job."
            elif best_count + better_count + good_count >= answered_questions * 0.5:
                performance_message = "Good effort."
            else:
                performance_message = "Keep practicing."
            
            # Build question review data
            questions_review = []
            for i, question in enumerate(prep_session.questions):
                user_answer = None
                evaluation = None
                for answer in prep_session.answers:
                    if answer.question_id == question.id:
                        user_answer = answer.user_answer
                        evaluation = answer.evaluation
                        break
                
                questions_review.append({
                    "index": i + 1,
                    "question": question.text,
                    "user_answer": user_answer,
                    "ideal_answer": question.ideal_answer,
                    "evaluation": evaluation
                })

            return jsonify({
                "mode": mode,
                "topic": prep_session.topic or "PDF-based session",
                "questions_attempted": answered_questions,
                "total_questions": total_questions,
                "good_count": good_count,
                "better_count": better_count,
                "best_count": best_count,
                "completion_percentage": completion_percentage,
                "performance_message": performance_message,
                "questions_review": questions_review
            }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to get session summary: {str(e)}"}), 500
