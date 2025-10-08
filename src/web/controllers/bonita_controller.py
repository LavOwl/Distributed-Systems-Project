from flask import Blueprint, jsonify
from src.web.services.bonita_service import BonitaService
from flask import render_template 
import os
from dataclasses import dataclass
from typing import List
from flask import request, jsonify

# Step 1: define classes
@dataclass
class Task:
    name: str
    start_date: str
    end_date: str
    category: str

@dataclass
class Project:
    title: str
    tasks: List[Task]



bonita_bp = Blueprint("APIbonita", __name__)
BONITA_BASE_URL = os.environ.get("BONITA_BASE_URL")


@bonita_bp.get("/")
def index():
    """
    Renderiza el formulario principal.
    """
    return render_template("index.html")



@bonita_bp.post("/v1/iniciar_proyecto")
def iniciar_proyecto():
    
    payload = request.get_json(silent=True) or {}
    # Do something with the tasks, and/or the Project, classes are down for changes, and they may be all added to the DB <3
    tasks = [
        Task(
            name=t.get("name", ""),
            start_date=t.get("startDate", ""),
            end_date=t.get("endDate", ""),
            category=t.get("category", "")
        )
        for t in payload.get("tasks", [])
    ]
    project = Project(title=payload.get("title", ""), tasks=tasks)

    process_id = iniciar_proceso('proceso_de_ejecucion')
    result = completar_tarea(process_id)
    return result

        
    
def iniciar_proceso(process_name: str):
    """
    Obtiene el ID del proceso enviado por parámetro y seguidamente lo inicia,
    devolviendo el case_id.
    """

    bonita = BonitaService()
    bonita.bonita_login()
    process_id = bonita.obtener_id_proceso(process_name)
    if not process_id:
        raise Exception()
    case_id = bonita.iniciar_proceso(process_id=process_id)
    return jsonify(case_id)


def completar_tarea(case_id):
    """
    Completa la primer tarea pendiente del case_id recibido por parámetro.
    """
    bonita = BonitaService()
    bonita.bonita_login()
    task_id = bonita.obtener_tarea_pendiente(case_id)
    if not task_id:
        raise Exception()
    result = bonita.completar_tarea(task_id)
    return result