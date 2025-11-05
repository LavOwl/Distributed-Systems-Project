from src.core.stage.model import Stage, CoverageRequest, StatusStage
from src.core.observation.model import Observation, Status
from src.core.project.model import Project
from src.core.database import db

def run():
    """
    Creación de las tablas iniciales.
    """

    # Creación de proyectos.
    project_1 = Project(
        case_id=123,
        name="Construcción de escuela",
        description="Proyecto para la construcción de una nueva escuela en la comunidad local."
    )

    project_2 = Project(
        case_id=1211,
        name="Construcción de comedor",
        description="Proyecto para la construcción del nuevo comedor universitario."
    )
    
    # Añadir proyectos a la sesión.
    db.session.add(project_1)
    db.session.add(project_2)

    # Creación de etapas.
    stage_1 = Stage(
        id_project=1,
        name="Relevamiento inicial",
        description="Visita al sitio y análisis de necesidades.",
        start_date="2025-01-10 00:00:00",
        end_date="2025-01-20 23:59:59",
        coverage_request=CoverageRequest.DINERO,
        status=StatusStage.PENDING,
        requires_contribution=True
    )
    
    stage_2 = Stage(
        id_project=1,
        name="Ejecución de obra",
        description="Construcción y desarrollo del proyecto.",
        start_date="2025-02-01 00:00:00",
        end_date="2025-06-30 23:59:59",
        coverage_request=CoverageRequest.MATERIALES,
        status=StatusStage.PENDING,
        requires_contribution=False
    )
    
    stage_3 = Stage(
        id_project=1,
        name="Finalización y entrega",
        description="Revisión final y entrega al cliente.", 
        start_date="2025-07-01 00:00:00",
        end_date="2025-07-15 23:59:59",
        coverage_request=CoverageRequest.MANO_DE_OBRA,
        status=StatusStage.PENDING,
        requires_contribution=True
    )
    
    stage_4 = Stage(
        id_project=2,
        name="Construcción de comedor",
        description="Se realiza la construcción del nuevo comedor universitario.", 
        start_date="2025-07-01 00:00:00",
        end_date="2025-08-15 23:59:59",
        coverage_request=CoverageRequest.MANO_DE_OBRA,
        status=StatusStage.PENDING,
        requires_contribution=True
    )
    
    stage_5 = Stage(
        id_project=2,
        name="Inspección final",
        description="Inspección y aprobación del comedor construido.",  
        start_date="2025-08-16 00:00:00",
        end_date="2025-08-31 23:59:59",
        coverage_request=CoverageRequest.DINERO,
        status=StatusStage.PENDING,
        requires_contribution=True
    )

    # Añadir observaciones a la sesión.
    db.session.add(stage_1)
    db.session.add(stage_2)
    db.session.add(stage_3)
    db.session.add(stage_4)
    db.session.add(stage_5)

    # Creación de observaciones.
    observation_1 = Observation(
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
    
    # Agregar observaciones a la sesión.
    db.session.add(observation_1)
    db.session.add(observation_2)
    
    # Almacenamiento de las tablas en la base de datos.
    db.session.commit()
    print("Tablas creadas correctamente ✅.")