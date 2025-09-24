from flask import Flask
from .config.config import get_config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app() -> Flask:
    app: Flask = Flask(__name__)

    app.config.from_object(get_config())

    db.init_app(app)

    @app.route("/")
    def home(): #type: ignore
        return "Flask + Postgres is working!"
    
    return app