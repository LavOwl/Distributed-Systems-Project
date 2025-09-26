from src import create_app
from flask import Flask, request, jsonify
from src.web.controllers.bonita_controller import bonita_bp

app = create_app()
app.register_blueprint(bonita_bp, url_prefix="/APIbonita")

if __name__ == '__main__':
    app.run()

# app = Flask(__name__)


# bonita = BonitaService()



