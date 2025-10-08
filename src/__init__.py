from flask import Flask
from flask_cors import CORS
from src.config.config import get_config
from src.core.database import db, create_tables
from src.web.blueprints import register_blueprints

# Creación de la app principal.
def create_app() -> Flask:
    app: Flask = Flask(__name__)

    # Seteo de configuración.
    app.config.from_object(get_config())
    CORS(app)
    db.init_app(app)
    create_tables(app)

    # Registro de blueprints.
    register_blueprints(app)

    # Renderización del home.
    @app.route("/")
    def home():
        return "Backend ejecutando correctamente ✅."
    
    return app