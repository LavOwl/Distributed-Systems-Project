from src import create_app
from flask import Flask, request, jsonify
from src.routes.bonita_api import bonita_bp
from src.servicios.bonita_service import BonitaService

app = create_app()
app.register_blueprint(bonita_bp, url_prefix="/APIbonita")

if __name__ == '__main__':
    app.run()

# app = Flask(__name__)


# bonita = BonitaService()



