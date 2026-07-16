"""Prep routes for PrepPal application."""
from flask import Blueprint, render_template, redirect, url_for, current_app

prep_bp = Blueprint("prep", __name__)


@prep_bp.route("/prep/<session_id>/loading")
def prep_loading(session_id: str):
    """Render the question generation loading page."""
    prep_session = current_app.session_service.get_session(session_id)
    if not prep_session:
        return redirect(url_for("home.index"))
    return render_template("loading.html", session_id=session_id)


@prep_bp.route("/prep/<session_id>")
def prep_session(session_id: str):
    """Render the question page for an active session."""
    prep_session = current_app.session_service.get_session(session_id)
    if not prep_session:
        return redirect(url_for("home.index"))
    if not current_app.session_service.is_questions_ready(session_id):
        return redirect(url_for("prep.prep_loading", session_id=session_id))
    if prep_session.is_complete:
        return redirect(url_for("prep.session_summary", session_id=session_id))
    return render_template("question.html", session_id=session_id)


@prep_bp.route("/prep/<session_id>/summary")
def session_summary(session_id: str):
    """Render the session summary page."""
    prep_session = current_app.session_service.get_session(session_id)
    if not prep_session:
        return redirect(url_for("home.index"))
    return render_template("summary.html", session_id=session_id)
