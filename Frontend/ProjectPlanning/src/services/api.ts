import type { Project, ApiError } from '../types/types';

const API_BASE_URL = 'http://localhost:5000';

class ApiService {
  private async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      switch (response.status) {
        case 401:
          throw { type: 'SESSION_EXPIRED', message: 'Sesión expirada o inválida' } as ApiError;
        case 403:
          throw { type: 'PERMISSION_DENIED', message: 'Permisos insuficientes' } as ApiError;
        default:
          throw { type: 'UNKNOWN_ERROR', message: `Error inesperado. Código: ${response.status}` } as ApiError;
      }
    }
    return response.json();
  }

  async getProjectsWithStages(): Promise<Project[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/project/v1/get_projects_with_stages`, {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      return await this.handleResponse<Project[]>(response);
    } catch (error) {
      if (error && typeof error === 'object' && 'type' in error) {
        throw error;
      }
      throw { 
        type: 'NETWORK_ERROR', 
        message: 'La conexión al servidor falló, por favor intentelo de nuevo.' 
      } as ApiError;
    }
  }

  async sendObservation({project_id, name, description} : {project_id:number, name:string, description:string}): Promise<string> {
    try {
      const response = await fetch(`${API_BASE_URL}/project/v1/add_observation/${project_id}`, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: name,
          description: description,
        }),
      });

      return await this.handleResponse<string>(response);
    } catch (error) {
      if (error && typeof error === 'object' && 'type' in error) {
        throw error;
      }
      throw { 
        type: 'NETWORK_ERROR', 
        message: 'La conexión al servidor falló, por favor intentelo de nuevo.'
      } as ApiError;
    }
  }

  async finalizarRevision(): Promise<{ message: string }> {
    try {
        const response = await fetch(`${API_BASE_URL}/project/v1/finalizar_revision`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        return await this.handleResponse<{ message: string }>(response);
    } catch (error) {
        if (error && typeof error === 'object' && 'type' in error) {
            throw error;
        }
        throw { 
            type: 'NETWORK_ERROR', 
            message: 'La conexión al servidor falló, por favor intentelo de nuevo.'
        } as ApiError;
    }
}

}

export const apiService = new ApiService();