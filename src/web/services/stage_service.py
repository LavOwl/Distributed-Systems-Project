import requests
from requests.exceptions import HTTPError, RequestException
from flask import jsonify
from src.core.stage import services
import os


def get_stages_project(project_id: int):
    """
    Obtiene las etapas asociadas a un proyecto.
    """
    
    stages = services.get_stages_by_project_id(project_id)
    
    return [stage.to_dict() for stage in stages]


def get_all_stages_by_project():
    """
    Obtiene todas las etapas de todos los proyectos.
    """
    
    stages = services.get_all_stages_by_project()
    
    return [stage.to_dict() for stage in stages]