from flask import Blueprint, jsonify
from src.web.services.bonita_service import BonitaService
from flask import render_template 
import os


bonita_bp = Blueprint("APIbonita", __name__)
BONITA_BASE_URL = os.environ.get("BONITA_BASE_URL")


@bonita_bp.get("/")
def index():
    """
    Renderiza el formulario principal.
    """
    return render_template("index.html")


@bonita_bp.get("/v1/login")
def login():
    """
    Realiza el login con Bonita.
    """
    bonita = BonitaService()
    session = bonita.bonita_login()
    if session:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Login failed"}), 401

    
@bonita_bp.post("/v1/iniciar_proceso/<process_name>")
def iniciar_proceso(process_name):
    """
    Obtiene el ID del proceso enviado por parámetro y seguidamente lo inicia,
    devolviendo el case_id.
    """
    bonita = BonitaService()
    bonita.bonita_login()
    process_id = bonita.obtener_id_proceso(process_name)
    if not process_id:
        return jsonify({"message": "No se pudo obtener el ID del proceso"}), 500
    case_id = bonita.iniciar_proceso(process_id=process_id)
    return jsonify(case_id)


@bonita_bp.get("/v1/obtener_id_proceso/<process_name>")
def obtener_id_proceso(process_name):
    """
    Devuelve el ID del proceso con nombre recibido por parámetro pero no lo inicia.
    """
    bonita = BonitaService()
    bonita.bonita_login()
    process_id = bonita.obtener_id_proceso(process_name)
    if process_id:
        return jsonify({"process_id": process_id}), 200
    else:
        return jsonify({"message": "Proceso no encontrado."}), 401


@bonita_bp.post("/v1/completar_tarea/<case_id>")
def completar_tarea(case_id):
    """
    Completa la primer tarea pendiente del case_id recibido por parámetro.
    """
    bonita = BonitaService()
    bonita.bonita_login()
    task_id = bonita.obtener_tarea_pendiente(case_id)
    if not task_id:
        return jsonify({"message": "No se puedo encontrar la tarea."}), 500
    result = bonita.completar_tarea(task_id)
    return jsonify(result)


@bonita_bp.get("/v1/obtener_tarea_pendiente/<case_id>")
def obtener_tarea_pendiente(case_id):
    """
    Obtiene la primer tarea pendiente dado un case_id recibido por parámetro.
    """
    bonita = BonitaService()
    bonita.bonita_login()
    task_id = bonita.obtener_tarea_pendiente(case_id)
    if task_id:
        return jsonify({"task_id": task_id}), 200
    else:
        return jsonify({"message": "Tarea no encontrada."}), 401