from flask import Blueprint, request, jsonify
from src.servicios.bonita_service import BonitaService
from flask import render_template 
import os

bonita_bp = Blueprint("APIbonita", __name__)
BONITA_BASE_URL = os.environ.get("BONITA_BASE_URL")

@bonita_bp.get("/")
def index():
    return render_template("index.html")

@bonita_bp.get("/v1/login")
def login():
    bonita = BonitaService()
    session = bonita.bonita_login()
    if session:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Login failed"}), 401
    

    
@bonita_bp.post("/v1/iniciar_proceso")
def iniciar_proceso():
    bonita = BonitaService()
    bonita.bonita_login()
    process_id = bonita.get_process_id()
    if not process_id:
        return jsonify({"message": "No se pudo obtener el ID del proceso"}), 500
    result = bonita.iniciar_proceso(process_id=process_id)
    print("Resultado de iniciar proceso:", result)
    return jsonify(result)

# @bonita_bp.route("/set_variable/<case_id>/<nombre>", methods=["PUT"])
# def set_variable(case_id, nombre):
#     data = request.json
#     valor = data.get("valor")
#     result = bonita.setear_variable(case_id, nombre, valor)
#     return jsonify(result)

@bonita_bp.get("/obtener_id_proceso")
def obtener_Id():
    bonita = BonitaService()
    bonita.bonita_login()
    result = bonita.get_process_id()
    
    if result:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Login failed"}), 401
    

@bonita_bp.post("/completar_tarea/<task_id>")
def completar_tarea(task_id):
    bonita = BonitaService()
    ok = bonita.completar_actividad(task_id)
    return jsonify({"success": ok})
