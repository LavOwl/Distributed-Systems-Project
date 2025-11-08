from src.web.services.bonita_service import BonitaService
from flask import request

def get_authenticated_bonita_service():
    """
    Recupera cookies de autenticación y devuelve un BonitaService configurado.
    Lanza ValueError si no hay cookies válidas.
    """
    csrf_token = request.cookies.get("X-Bonita-API-Token")
    jsessionid = request.cookies.get("JSESSIONID")

    if not csrf_token or not jsessionid:
        raise ValueError("Sesión de Bonita no válida o expirada")

    bonita = BonitaService()
    bonita.csrf_token = csrf_token
    bonita.session.cookies.set("JSESSIONID", jsessionid)
    bonita.session.cookies.set("X-Bonita-API-Token", csrf_token)

    return bonita