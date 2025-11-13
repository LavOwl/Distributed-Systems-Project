import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/api';
import type { Observation, Status } from '../../types/types';

export function ProjectObservations() {
  const [observations, setObservations] = useState<Observation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [warning, setWarning] = useState<{type:'SUCCESS' | 'FAILURE', message:string} | null>(null);

  useEffect(() => {
    loadObservations();
  }, []);

  const loadObservations = async () => {
    try {
      setLoading(true);
      setError(null);
      const observationsData = await apiService.getObservationsByUser();
      setObservations(observationsData);
    } catch (err: any) {
      console.error('Error loading observations:', err);
      if (err.type === 'NOT_FOUND') {
        setError('No se encontraron observaciones asociadas a tus proyectos.');
      } else if (err.message) {
        setError(err.message);
      } else {
        setError('Ocurrió un error al cargar las observaciones.');
      }
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: Status) => {
    switch (status) {
      case 'PENDING':
        return 'bg-yellow-100 text-yellow-800';
      case 'IN_PROGRESS':
        return 'bg-blue-100 text-blue-800';
      case 'RESOLVED':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: Status) => {
    switch (status) {
      case 'PENDING':
        return 'Pendiente';
      case 'IN_PROGRESS':
        return 'En Progreso';
      case 'RESOLVED':
        return 'Resuelta';
      default:
        return status;
    }
  };

  const markAsSolved = async (observation_id:number) => {
    setWarning(null);
    try {
        const result = await apiService.finalizarObservacion(observation_id);
        setWarning({type:'SUCCESS', message:'Observacion resuelta exitosamente.'})
    } catch (error: any) {
        if (error?.type === 'SESSION_EXPIRED') {
            setWarning({type:'FAILURE', message:'La sesión ha expirado. Por favor, inicie sesión nuevamente.'});
        } else if (error?.type === 'PERMISSION_DENIED') {
            setWarning({type:'FAILURE', message:'No tiene permisos para resolver observaciones.'});
        } else if (error?.type === 'NETWORK_ERROR') {
            setWarning({type:'FAILURE', message:'Error de conexión. Por favor, inténtelo de nuevo.'});
        } else if (error?.message) {
            setWarning(error.message);
        } else {
            setWarning({type:'FAILURE', message:'Ocurrió un error inesperado al resolver la observación.'});
        }
    }
  }

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 text-center">
        <p className="text-gray-500">Cargando observaciones...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow p-6 text-center">
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-red-700">{error}</p>
          <button
            onClick={loadObservations}
            className="mt-2 bg-red-100 text-red-800 px-3 py-1 rounded text-sm font-medium hover:bg-red-200"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 w-4/5">
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
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Observaciones Recibidas</h2>
      </div>

      {observations.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <p className="text-gray-500">No hay observaciones para mostrar.</p>
        </div>
      ) : (
        <div className="space-y-4 flex gap-4 flex-wrap">
          {observations.map((observation) => (
            <div key={observation.id} className="bg-white rounded-lg shadow border border-gray-200 p-6 w-90 h-65">
              <div className="flex justify-between items-start mb-4">
                <div className="flex-1">
                  <h3 className="text-md font-semibold text-gray-800">{observation.name}</h3>
                  {observation.project_name && (
                    <p className="text-xs text-gray-600 mt-1">
                      Proyecto: {observation.project_name}
                    </p>
                  )}
                </div>
                <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(observation.status)}`}>
                  {getStatusText(observation.status)}
                </span>
              </div>

              {observation.description && (
                <p className="text-gray-700 mb-4 text-sm overflow-auto h-25">{observation.description}</p>
              )}

              <div className="flex justify-between items-center text-sm text-gray-600">
                <button className="px-4 hover:bg-green-100 w-fit cursor-pointer duration-200 h-9 border-2 border-green-800 text-black text-sm rounded-sm" onClick={() => markAsSolved(observation.id)}>Marcar como resuelta</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}