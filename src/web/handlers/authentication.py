from src.web.services.bonita_service import BonitaService
from flask import request, jsonify, g
from functools import wraps

def require_bonita_auth(grupo_requerido=None):
    """
    Decorador para verificar que el usuario tenga una sesión válida en Bonita
    y, opcionalmente, que pertenezca a un grupo específico.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            bonita = BonitaService()

            jsessionid = request.cookies.get("JSESSIONID")
            token = request.cookies.get("X-Bonita-API-Token")

            if not jsessionid or not token:
                return jsonify({"error": "Sesión no encontrada. Inicie sesión nuevamente."}), 401

            bonita.session.cookies.set("JSESSIONID", jsessionid)
            bonita.session.cookies.set("X-Bonita-API-Token", token)
            bonita.csrf_token = token

            try:
                info = bonita.obtener_info_usuario()
                g.bonita_user = info

                if grupo_requerido:
                    grupos = bonita.obtener_grupos_usuario(info["user_id"])
                    if grupo_requerido not in grupos:
                        return jsonify({"error": f"El usuario no tiene permisos para acceder."}), 403

            except Exception:
                return jsonify({"error": "Sesión expirada o inválida."}), 401

            return f(*args, **kwargs)
        return decorated_function
    return decorator