from src.web.services.bonita_service import BonitaService
from flask import Blueprint, request, jsonify
import os

bonita_bp = Blueprint("bonita", __name__)
BONITA_BASE_URL = os.environ.get("BONITA_BASE_URL")

@bonita_bp.post("/v1/login")
def bonita_login():
    """
    Realiza el login en Bonita y devuelve un mensaje de éxito o error.
    (1) Recibe (JSON en el BODY):
        1. username: string.
        2. password: string.
    (2) Devuelve:
        1. 200 - message: login exitoso.
        2. 401 - error: usuario o contraseña incorrectos.
    """
    # Recibe el JSON del body, y hace el login con Bonita.
    data = request.get_json(silent=True) or {}
    bonita = BonitaService()
    session = bonita.bonita_login(data)

    # Verifica si se puede autenticar correctamente.
    if not session:
            return jsonify({"error": "Usuario o contraseña incorrectos."}), 401
    
    # Obtiene las cookies desde la sesión.
    jsessionid = session.cookies.get("JSESSIONID")
    token = session.cookies.get("X-Bonita-API-Token")

    # Setear las cookies para el cliente.
    response = jsonify({"message": "Login exitoso"})
    response.set_cookie("JSESSIONID", jsessionid)
    response.set_cookie("X-Bonita-API-Token", token)
    return response, 200