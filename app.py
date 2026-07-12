"""Main application factory for PrepPal."""
from flask import Flask
from config import Config
from routes.home import home_bp
from routes.prep import prep_bp
from routes.api import api_bp
from services.ai_service import AIService
from services.pdf_service import PDFService
from services.session_service import SessionService
from services.prep_service import PrepService
from services.evaluation_service import EvaluationService


def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    Args:
        config_class: Configuration class to use

    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.ai_service = AIService(
        api_key=app.config.get('NVIDIA_API_KEY'),
        base_url=app.config.get('NVIDIA_BASE_URL')
    )
    app.pdf_service = PDFService(upload_dir=app.config.get('UPLOAD_FOLDER'))
    app.session_service = SessionService()
    app.prep_service = PrepService(
        session_service=app.session_service,
        ai_service=app.ai_service,
        pdf_service=app.pdf_service
    )
    app.evaluation_service = EvaluationService(ai_service=app.ai_service)

    app.register_blueprint(home_bp)
    app.register_blueprint(prep_bp)
    app.register_blueprint(api_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
