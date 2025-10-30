from src.core.stage.model import Stage, CoverageRequest, StatusStage
from src.core.observation.model import Observation, Status
from src.core.project.model import Project
from src.core.database import db

def run():
    """
    Creación de las tablas iniciales.
    """

    project = Project(
        case_id=123,
        name="Construcción de escuela",
        description="Proyecto para la construcción de una nueva escuela en la comunidad local."
    )
    
    db.session.add(project)

    stage = Stage(
        id_project=1,
        name="Relevamiento inicial",
        description="Visita al sitio y análisis de necesidades.",
        start_date="2025-01-10 00:00:00",
        end_date="2025-01-20 23:59:59",
        coverage_request=CoverageRequest.DINERO,
        status=StatusStage.PENDING
    )
    
    stage_2 = Stage(
        id_project=1,
        name="Ejecución de obra",
        description="Construcción y desarrollo del proyecto.",
        start_date="2025-02-01 00:00:00",
        end_date="2025-06-30 23:59:59",
        coverage_request=CoverageRequest.MATERIALES,
        status=StatusStage.PENDING
    )
    
    stage_3 = Stage(
        id_project=1,
        name="Finalización y entrega",
        description="Revisión final y entrega al cliente.", 
        start_date="2025-07-01 00:00:00",
        end_date="2025-07-15 23:59:59",
        coverage_request=CoverageRequest.MANO_DE_OBRA,
        status=StatusStage.PENDING
    )

    observation = Observation(
        id_project=1,
        name="Revisar planos",
        description="Verificar planos enviados por el cliente.",
        status=Status.PENDING
    )
    
    observation_2 = Observation(
        id_project=1,
        name="Aprobar presupuesto",
        description="Confirmar aprobación del presupuesto inicial.",
        status=Status.PENDING
    )
    
    # Agregar stage y observation a la sesión.
    db.session.add(stage)
    db.session.add(stage_2)
    db.session.add(stage_3)
    db.session.add(observation_2)
    db.session.add(observation)
    
    # Almacenamiento de las tablas en la base de datos.
    db.session.commit()
    print("Tablas creadas correctamente ✅.")