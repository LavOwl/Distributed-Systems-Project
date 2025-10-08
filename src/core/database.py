from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

def init_app(app):
    """
    Inicia la base de datos con la aplicación de flask.
    """
    db.init_app(app)
    config(app)
    return app


def config(app):
    """
    Configuración de hooks para la base de datos.
    """
    @app.teardown_appcontext
    def close_session(exception=None):
        db.session.close()
    return app


def reset(app):
    """
    Resetea la base de datos.
    """
    with app.app_context():
        print("Eliminando base de datos...")
        db.drop_all()
        print("Creando base de datos nuevamente...")
        db.create_all()
        db.session.commit()
        print("Tablas creadas ✅.")