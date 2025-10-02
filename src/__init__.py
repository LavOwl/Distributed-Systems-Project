from flask import Flask
from .config.config import get_config
from flask_sqlalchemy import SQLAlchemy
from src.web.controllers.bonita_controller import bonita_bp
from flask_cors import CORS

db = SQLAlchemy()

def create_app() -> Flask:
    app: Flask = Flask(__name__)

    app.config.from_object(get_config())
    CORS(app)
    db.init_app(app)


    app.register_blueprint(bonita_bp, url_prefix="/APIbonita")
    @app.route("/")
    def home(): #type: ignore
        return "Flask + Postgres is working!"
    
    return app