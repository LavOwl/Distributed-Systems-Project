from flask import Blueprint, request, jsonify
from src.servicios.bonita_service import BonitaService
from flask import render_template 


bonita_bp = Blueprint("bonita", __name__)


@bonita_bp.get("/")
def index():
    return render_template("index.html")

@bonita_bp.get("/login")
def login():
    bonita = BonitaService()
    session = bonita.bonita_login("http://localhost:8080/bonita/","walter.bates", "bpm")
    if session:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Login failed"}), 401
    
    
    
@bonita_bp.post("/iniciar_proceso/<process_id>")
def iniciar_proceso(process_id):
    bonita = BonitaService()
    result = bonita.iniciar_proceso(process_id)
    return jsonify(result)

# @bonita_bp.route("/set_variable/<case_id>/<nombre>", methods=["PUT"])
# def set_variable(case_id, nombre):
#     data = request.json
#     valor = data.get("valor")
#     result = bonita.setear_variable(case_id, nombre, valor)
#     return jsonify(result)

@bonita_bp.post("/completar_tarea/<task_id>")
def completar_tarea(task_id):
    bonita = BonitaService()
    ok = bonita.completar_actividad(task_id)
    return jsonify({"success": ok})
