from flask import Blueprint, request
from src.web.services.bonita_service import BonitaService
import os

bonita_bp = Blueprint("APIbonita", __name__)
BONITA_BASE_URL = os.environ.get("BONITA_BASE_URL")

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

    process_id = BonitaService.obtener_id_proceso('proceso_de_ejecucion')
    result = completar_tarea(process_id)
    return result