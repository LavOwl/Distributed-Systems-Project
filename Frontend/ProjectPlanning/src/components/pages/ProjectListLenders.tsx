import { useState, useEffect } from 'react';
import type { Stage, ApiError, StatusStage, CoverageRequest } from '../../types/types';
import { apiService } from '../../services/api';

export function ProjectListLenders(){
  const [stages, setStages] = useState<Stage[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);
  const [warning, setWarning] = useState<{type:'SUCCESS' | 'FAILURE', message:string} | null>(null);

  useEffect(() => {
    fetchstages();
  }, []);

  const fetchstages = async () => {
    try {
      setLoading(true);
      setError(null);
      const stagesData = await apiService.getAvailableStages();
      setStages(stagesData);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  };

  const groupedStages = stages.reduce((acc, stage) => {
    const projectId = stage.id_project;
    if (!acc[projectId]) {
        acc[projectId] = {
        projectId: projectId,
        stages: []
        };
    }
    acc[projectId].stages.push(stage);
    return acc;
    }, {} as Record<number, { projectId: number; stages: Stage[] }>);

  const groupedStagesArray = Object.values(groupedStages);

  const contributeToStage = async (stage_id:number) => {
    try{
        const response = await apiService.confirmContribution(stage_id);
        setWarning({type: "SUCCESS", message: "Contribución registrada!"})
        setStages(stages => 
          stages.filter(s => s.id !== stage_id)
        );
    }
    catch (error: any) {
        if (error?.type === 'SESSION_EXPIRED') {
            setWarning({type:'FAILURE', message:'La sesión ha expirado. Por favor, inicie sesión nuevamente.'});
        } else if (error?.type === 'PERMISSION_DENIED') {
            setWarning({type:'FAILURE', message:'No tiene permisos para .'});
        } else if (error?.type === 'NETWORK_ERROR') {
            setWarning({type:'FAILURE', message:'Error de conexión. Por favor, inténtelo de nuevo.'});
        } else if (error?.message) {
            setWarning(error.message);
        } else {
            setWarning({type:'FAILURE', message:'Ocurrió un error inesperado al intentar confirmar la contribución.'});
        }
    }
  };

  const getStatusColor = (status: StatusStage): string => {
    switch (status) {
      case "PENDING":
        return 'bg-yellow-100 text-yellow-800';
      case "IN_PROGRESS":
        return 'bg-blue-100 text-blue-800';
      case "FINISHED":
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getCoverageRequestColor = (coverage: CoverageRequest): string => {
    switch (coverage) {
      case "DINERO":
        return 'bg-purple-100 text-purple-800';
      case "MATERIALES":
        return 'bg-orange-100 text-orange-800';
      case "MANO_DE_OBRA":
        return 'bg-teal-100 text-teal-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  

  const renderError = () => {
    if (!error) return null;

    const errorConfig = {
      SESSION_EXPIRED: {
        title: 'Sesión expirada',
        message: 'Tu sesión ha expirado. Por favor inicie sesión.',
        action: () => window.location.href = '/login'
      },
      PERMISSION_DENIED: {
        title: 'Acceso denegado',
        message: 'Tus permisos actuales son insuficientes para visualizar esta página.',
        action: null
      },
      NETWORK_ERROR: {
        title: 'Fallo al conectarse',
        message: error.message,
        action: () => fetchstages()
      },
      UNKNOWN_ERROR: {
        title: 'Error',
        message: error.message,
        action: () => fetchstages()
      },
      NOT_FOUND: {
        title: 'Not Found',
        message: 'No hay etapas a las que contribuir aún.',
        action: () => fetchstages()
      }
    };

     const config = error.type in errorConfig ? errorConfig[error.type as keyof typeof errorConfig] : errorConfig.UNKNOWN_ERROR;

    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-4">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-sm font-medium text-red-800">
              {config.title}
            </h3>
            <div className="mt-2 text-sm text-red-700">
              <p>{config.message}</p>
            </div>
            {config.action && (
              <div className="mt-4">
                <button
                  type="button"
                  onClick={config.action}
                  className="bg-red-100 text-red-800 px-3 py-2 rounded text-sm font-medium hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                >
                  {error.type === 'SESSION_EXPIRED' ? 'Iniciar Sesión' : 'Reintentar'}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        {renderError()}
      </div>
    );
  }

  return (
    <>
      <div className='mx-auto w-4/5'>
        {warning && <div>
          <div className='fixed top-0 left-0 w-full h-full bg-black/20 z-0'></div>
          <div className={`border fixed top-1/2 left-1/2 transform -translate-1/2 z-10 rounded-md p-4 mb-4 ${
            warning.type === 'SUCCESS' 
              ? 'bg-green-50 border-green-200' 
              : 'bg-red-50 border-red-200'
          }`}>
            <div className="flex">
              <div className="flex-shrink-0">
                {warning.type === 'SUCCESS' ? (
                  <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                )}
              </div>
              <div className="ml-3">
                <h3 className={`text-sm font-medium ${
                  warning.type === 'SUCCESS' ? 'text-green-800' : 'text-red-800'
                }`}>
                  {warning.type === 'SUCCESS' ? 'Operación exitosa.' : 'Ha ocurrido un error confirmando la contribución.'}
                </h3>
                <div className={`mt-2 text-sm ${
                  warning.type === 'SUCCESS' ? 'text-green-700' : 'text-red-700'
                }`}>
                  <p>{warning.message}</p>
                </div>
                <div className="mt-4">
                  <button
                    type="button"
                    onClick={() => setWarning(null)}
                    className={`px-3 py-2 rounded text-sm font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                      warning.type === 'SUCCESS' 
                        ? 'bg-green-100 text-green-800 hover:bg-green-200 focus:ring-green-500' 
                        : 'bg-red-100 text-red-800 hover:bg-red-200 focus:ring-red-500'
                    }`}
                  >
                    Aceptar
                  </button>
                </div>
              </div>
            </div>
          </div>
          </div>
        }

        <div className="container w-full mx-auto">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900">Etapas</h1>
            <p className="text-gray-600 mt-2">Etapas por proyecto que solicitan contribución.</p>
          </div>

          {stages.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-6 text-center">
                <p className="text-gray-500">No hay etapas disponibles.</p>
            </div>
            ) : (
            <div className="space-y-6">
                {groupedStagesArray.map((projectGroup) => (
                <div key={projectGroup.projectId} className="bg-white rounded-lg shadow overflow-hidden">
                    <div className="p-6 border-b border-gray-200">
                    <h2 className="text-xl font-semibold text-gray-800">
                        Proyecto #{projectGroup.projectId}
                    </h2>
                    <p className="text-gray-600 mt-1">
                        Este proyecto requiere contribuciones para {projectGroup.stages.length} etapa{projectGroup.stages.length !== 1 ? 's' : ''}.
                    </p>
                    </div>
                    
                    <div className="p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Etapas del Proyecto</h3>
                    <div className="space-y-4">
                        {projectGroup.stages.map((stage) => (
                        <div key={stage.id} className="border border-gray-200 rounded-lg p-4">
                            <div className="flex justify-between items-start mb-2">
                            <h4 className="text-md font-medium text-gray-800">{stage.name}</h4>
                            <div className="flex space-x-2">
                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(stage.status)}`}>
                                {stage.status}
                                </span>
                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getCoverageRequestColor(stage.coverage_request)}`}>
                                {stage.coverage_request}
                                </span>
                            </div>
                            </div>
                            
                            {stage.description && (
                            <p className="text-gray-600 text-sm mb-3">{stage.description}</p>
                            )}
                            
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-fit text-sm text-gray-600">
                            <div>
                                <span className="font-medium">Fecha de inicio:</span>{' '}
                                {stage.start_date ? new Date(stage.start_date).toLocaleDateString() : 'N/A'}
                            </div>
                            <div>
                                <span className="font-medium">Fecha de fin estimada:</span>{' '}
                                {stage.end_date ? new Date(stage.end_date).toLocaleDateString() : 'N/A'}
                            </div>
                            <div>
                                <span className="font-medium">Requiere contribución:</span>{' '}
                                {stage.requires_contribution ? 'Sí' : 'No'}
                            </div>
                            <button className="px-4 hover:bg-green-100 w-fit cursor-pointer duration-200 h-9 border-2 border-green-800 text-black text-sm rounded-sm" onClick={() => contributeToStage(stage.id)}>Cubrir Contribución</button>
                            </div>
                        </div>
                        ))}
                    </div>
                    </div>
                </div>
                ))}
            </div>
            )}
        </div>
      </div>
    </>
  );
};