"""Prep routes for PrepPal application (question interface)."""
from flask import Blueprint, render_template

prep_bp = Blueprint("prep", __name__)


@prep_bp.route("/prep/<session_id>")
def prep_session(session_id: str):
    """Render the preparation session page."""
    # TODO: Implement actual session page rendering
    return render_template("index.html")  # Placeholder
