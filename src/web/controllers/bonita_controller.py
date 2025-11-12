from flask import Blueprint, request, jsonify, render_template, make_response, redirect, url_for, session
from src.web.services.bonita_service import BonitaService
import os

bonita_bp = Blueprint("bonita", __name__)
BONITA_BASE_URL = os.environ.get("BONITA_BASE_URL")

@bonita_bp.get("/v1/login")
def login_form():
    """
    Renderiza el template principal de login.
    (1) Recibe: 
        1. Nada.
    (2) Devuelve:
        1. Renderiza template /auth/login.html.
    """
    return render_template("auth/login.html")


@bonita_bp.post("/v1/login")
def bonita_login():
    """ 
    Realiza el login en Bonita y guarda los datos del usuario en sesión.
    (1) Recibe (form-data): 
        1. username: string 
        2. password: string 
    (2) Devuelve:
        1. Template /auth/login.html en caso de error.
        2. Template home.html en caso de éxito.
    """
    username = request.form.get("username")
    password = request.form.get("password")
    bonita = BonitaService()
    session_bonita = bonita.bonita_login({"username": username, "password": password})
    if not session_bonita:
        return render_template("auth/login.html", error="Usuario o contraseña incorrectos.")

    # Guarda cookies de la sesión de Bonita.
    jsessionid = session_bonita.cookies.get("JSESSIONID")
    token = session_bonita.cookies.get("X-Bonita-API-Token")
    response = make_response(redirect(url_for("home")))
    response.set_cookie("JSESSIONID", jsessionid)
    response.set_cookie("X-Bonita-API-Token", token)

    # Obtiene información del usuario y su rol.
    bonita.session = session_bonita
    bonita.csrf_token = token
    try:
        user_info = bonita.obtener_info_usuario()
        user_id = user_info["user_id"]
        grupos = bonita.obtener_grupos_usuario(user_id)
        role = grupos[0] if grupos else None
    except Exception:
        return render_template("auth/login.html", error="Error al obtener información del usuario.")

    # Guarda la sesión en Flask.
    session["logged_in"] = True
    session["username"] = username
    session["user_id"] = user_id
    session["role"] = role
    session["jsessionid"] = jsessionid
    session["token"] = token
    return response


@bonita_bp.get("/logout")
def logout():
    """
    Realiza el cierre de sesión en Bonita.
    (1) Recibe:
        1. Nada.
    (2) Devuelve:
        2. Renderiza template /auth/login.html. 
    """
    session.clear()
    return redirect(url_for("bonita.login_form"))