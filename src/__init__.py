from src.web.blueprints import register_blueprints
from src.config.config import get_config
from src.core.database import db, reset
from src.core import seed_data
from flask_cors import CORS
from flask import Flask

# Creación de la app principal.
def create_app() -> Flask:
    app: Flask = Flask(__name__)

    # Seteo de configuración.
    app.config.from_object(get_config())
      # CORS en una sola línea
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True, allow_headers=["Content-Type", "Authorization"])

    
    # Inicialización de la base de datos.
    db.init_app(app)

    # Registro de blueprints.
    register_blueprints(app)

    # Comando para borrar y crear las tablas de la base de datos nuevamente.
    @app.cli.command(name="reset-db")
    def reset_db():
        reset(app)

    # Comando para crear las tablas principales.
    @app.cli.command(name="seed-data")
    def seed_basic():
        seed_data.run()

    # Renderización del home.
    @app.route("/")
    def home():
        return "Backend ejecutando correctamente ✅."
    
    @app.cli.command("debug-uri")
    def debug_uri():
        print("=== DATABASE URI DEBUG ===")
        uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        print(f"URI: {uri}")
        print(f"URI length: {len(uri)}")
        print(f"URI as bytes: {uri.encode('utf-8')}")
        
        # Verificar caracteres problemáticos.
        for i, char in enumerate(uri):
            try:
                char.encode('utf-8')
            except UnicodeEncodeError:
                print(f"❌ Carácter problemático en posición {i}: '{char}' (hex: {ord(char):x})")
    
    return app