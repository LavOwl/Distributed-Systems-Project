import { useState, useEffect } from 'react';
import type { Project, ApiError, StatusStage, CoverageRequest } from '../../types/types';
import { apiService } from '../../services/api';
import { ObservationButton } from '../forms/ObservationButton';

export function ProjectListDirectives(){
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<ApiError | null>(null);
  const [warning, setWarning] = useState<{type:'SUCCESS' | 'FAILURE', message:string} | null>(null);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      setLoading(true);
      setError(null);
      const projectsData = await apiService.getProjectsWithStages();
      setProjects(projectsData);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
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
        action: () => fetchProjects()
      },
      UNKNOWN_ERROR: {
        title: 'Error',
        message: error.message,
        action: () => fetchProjects()
      },
      NOT_FOUND: {
        title: 'Not Found',
        message: 'No hay etapas a las que contribuir aún.',
        action: () => fetchProjects()
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
  
  const handleFinalizarRevision = async () => {
        setWarning(null);
        try {
            const result = await apiService.finalizarRevision();
            setWarning({type:'SUCCESS', message:'Observaciones concluidas exitosamente.'})
        } catch (error: any) {
            if (error?.type === 'SESSION_EXPIRED') {
                setWarning({type:'FAILURE', message:'La sesión ha expirado. Por favor, inicie sesión nuevamente.'});
            } else if (error?.type === 'PERMISSION_DENIED') {
                setWarning({type:'FAILURE', message:'No tiene permisos para finalizar la revisión.'});
            } else if (error?.type === 'NETWORK_ERROR') {
                setWarning({type:'FAILURE', message:'Error de conexión. Por favor, inténtelo de nuevo.'});
            } else if (error?.message) {
                setWarning(error.message);
            } else {
                setWarning({type:'FAILURE', message:'Ocurrió un error inesperado al finalizar la revisión.'});
            }
        }
    };

  return (
    <>
      <div className='mx-auto w-4/5'>
        {warning && 
          <div className={`border rounded-md p-4 mb-4 ${
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
                  {warning.type === 'SUCCESS' ? 'Operación exitosa.' : 'Ha ocurrido un error concluyendo las observaciones.'}
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
        }

        <div className="container w-full mx-auto">
          <button onClick={handleFinalizarRevision} className="px-4 hover:bg-red-100 float-end cursor-pointer duration-200 h-9 border-2 border-red-800 text-black text-sm rounded-sm">Concluir Observaciones</button>
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900">Proyectos</h1>
            <p className="text-gray-600 mt-2">Proyectos y sus etapas</p>
          </div>

          {projects.length === 0 ? (
            <div className="bg-white rounded-lg shadow p-6 text-center">
              <p className="text-gray-500">No hay proyectos aún.</p>
            </div>
          ) : (
            <div className="space-y-6">
              {projects.map((project) => (
                <div key={project.id} className="bg-white rounded-lg shadow overflow-hidden">
                  <div className="p-6 border-b flex justify-between border-gray-200">
                    <div>
                      <h2 className="text-xl font-semibold text-gray-800">{project.name}</h2>
                      <p className="text-gray-600 mt-1">{project.description}</p>
                    </div>
                    <div className='flex flex-col gap-4'>
                      <ObservationButton project_id={project.id}/>
                    </div>
                  </div>
                  
                  <div className="p-6">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Etapas</h3>
                    <div className="space-y-4">
                      {project.stages.map((stage) => (
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