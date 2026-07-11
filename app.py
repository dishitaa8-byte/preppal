"""Main application factory for PrepPal."""
from flask import Flask
from config import Config
from routes.home import home_bp
from routes.prep import prep_bp
from routes.api import api_bp


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
    
    # Initialize services (singletons for now)
    # In a production app, consider using a dependency injection container
    with app.app_context():
        # We'll set up services in app context if needed later
        pass
    
    # Register blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(prep_bp)
    app.register_blueprint(api_bp)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
