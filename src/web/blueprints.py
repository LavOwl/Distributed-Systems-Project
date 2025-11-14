from src.web.controllers.bonita_controller import bonita_bp
from src.web.controllers.stage_controller import stage_bp
from src.web.controllers.project_controller import project_bp
from src.web.controllers.monitoring_controller import monitor_bp

def register_blueprints(app):
    """
    Registra todos los blueprints de la aplicación.
    """
    app.register_blueprint(bonita_bp, url_prefix="/bonita")
    app.register_blueprint(stage_bp, url_prefix="/stage")
    app.register_blueprint(project_bp, url_prefix="/project")
    app.register_blueprint(monitor_bp, url_prefix="/monitor")