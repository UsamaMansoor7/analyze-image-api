from flask import Flask
from .api.image_analyzer import analyzer_bp
from .extensions import openai
#image_insight_api
def create_app(config_object="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initialize extensions
    openai.init_app(app)

    # Register blueprints
    app.register_blueprint(analyzer_bp)

    return app
