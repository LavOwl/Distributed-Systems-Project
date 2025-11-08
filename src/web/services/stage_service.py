from src.core.stage import services

def get_stages_project(project_id: int):
    """
    Obtiene las etapas asociadas a un proyecto.
    """
    stages = services.get_stages_by_project_id(project_id)
    return [stage.to_dict() for stage in stages]


def get_all_stages_by_project():
    """
    Obtiene todas las etapas pendientes de todos los proyectos.
    """
    stages = services.get_all_stages_by_project()
    return [stage.to_dict() for stage in stages]


def cover_stage(stage_id: int):
    """
    Cubre una etapa específica según su ID.
    """
    stage = services.get_pending_stage_by_id(stage_id)
    if not stage:
        return None
    return services.cover_stage(stage)


def get_case_id_by_stage(stage):
    """
    Obtiene el case_id del proyecto al que pertenece una etapa.
    """
    if not stage or not stage.project:
        return None
    return stage.project.case_id