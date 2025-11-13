from flask import Flask, render_template, g, session
from src.web.blueprints import register_blueprints
from src.config.config import get_config
from src.core.database import db, reset
from src.core import seed_data
from flask_cors import CORS
from pathlib import Path

# Creación de la app principal.
def create_app() -> Flask:
    # Ruta a los templates y archivos estáticos.
    base_path = Path(__file__).parent
    templates_path = base_path / "web" / "templates"
    static_path = base_path / "web" / "static"

    # Creación de la APP flask tomando las carpetas para los templates.
    app: Flask = Flask(
        __name__,
        template_folder=str(templates_path),
        static_folder=str(static_path)
    )

    # Seteo de configuración.
    app.config.from_object(get_config())
    CORS(app, 
     origins=["http://localhost:5173"],
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"]
    )
    
    db.init_app(app)

    # Almacenamiento de datos de la sesión del usuario.
    @app.before_request
    def load_logged_in_user():
        g.user = session.get("username")
        g.role = session.get("role")
        g.logged_in = session.get("logged_in", False)

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
        return render_template("home.html")
    
    @app.cli.command("debug-uri")
    def debug_uri():
        print("=== DATABASE URI DEBUG ===")
        uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        print(f"URI: {uri}")
        print(f"URI length: {len(uri)}")
        print(f"URI as bytes: {uri.encode('utf-8')}")
        
        # Verificar caracteres problemáticos
        for i, char in enumerate(uri):
            try:
                char.encode('utf-8')
            except UnicodeEncodeError:
                print(f"❌ Carácter problemático en posición {i}: '{char}' (hex: {ord(char):x})")
    
    return app