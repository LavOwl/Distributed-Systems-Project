from src.web.controllers.bonita_controller import bonita_bp

def register_blueprints(app):
    """
    Registra todos los blueprints de la aplicación.
    """
    app.register_blueprint(bonita_bp, url_prefix="/APIbonita")