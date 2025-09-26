import requests
from requests.exceptions import HTTPError, RequestException
import os


BONITA_URL = os.getenv("BONITA_BASE_URL", "http://localhost:8080/bonita").rstrip("/")
BONITA_USER = os.getenv("BONITA_USER", "walter.bates")
BONITA_PASS = os.getenv("BONITA_PASSWORD", "bpm")


class BonitaService:
    def __init__(self):
        self.base_url = BONITA_URL
        self.username =  BONITA_USER
        self.password =  BONITA_PASS
        self.session = requests.Session()
        self.csrf_token = None


    def bonita_login(self):
        """
        Se conecta al loginservice de Bonita y devuelve una sesión de requests 
        con las cookies de autenticación.
        """

        # Si faltan variables lanza una excepción.
        if not self.base_url or not self.username or not self.password:
            raise ValueError("BONITA_URL, BONITA_USER o BONITA_PASS no están configurados.")
        
        # Prepara los datos de la url y de los headers para hacer la petición.
        login_url = f"{self.base_url}/loginservice"
        login_data = {
            'username': self.username,
            'password': self.password,
            'redirect': 'false'
        }
        self.session = requests.Session()

        try:

            # Realiza la petición POST con los datos previamente guardados.
            response = self.session.post(
                login_url,
                data=login_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

            # Levanta una excepción para los errores del tipo 4xx y 5xx.
            response.raise_for_status()

            # Guarda el token de la sesión en la variable de instancia.
            token = self.session.cookies.get("X-Bonita-API-Token")
            if not token:
                raise RuntimeError("No se recibió token de Bonita después del login.")
            self.csrf_token = token
            return self.session
        except (HTTPError, RequestException, ValueError):
            return False


    def obtener_id_proceso(self, name_process):
        """
        Obtiene el ID del proceso recibido por parámetro.
        """
        # Prepara los datos para la petición.
        url = f"{self.base_url}/API/bpm/process"
        params = {
            'name': name_process
        }
        headers = {
            'X-Bonita-API-Token': self.csrf_token
        }

        # Realiza la petición GET.
        response = self.session.get(url, params=params, headers=headers)

        # Levanta una excepción para los errores 4xx y 5xx.
        response.raise_for_status()

        # Busco dentro del listado de procesos el que coincida con el nombre y devuelvo su ID.
        for process in response.json():
            if process['name'] == name_process:
                return process['id']


    def iniciar_proceso(self, process_id):
        """
        Recibe un ID de proceso y lo inicia.
        """

        # Prepara los datos para hacer la petición.
        url = f"{self.base_url}/API/bpm/process/{process_id}/instantiation"
        headers = {
            'content-type': 'application/json',
            'X-Bonita-API-Token': self.csrf_token
        }

        # Realiza la petición.
        response = self.session.post(url, headers=headers)

        # Levanta una excepción para los errores 4xx y 5xx.
        response.raise_for_status()

        # Devuelve un JSON con la respuesta.
        return response.json()


    def completar_actividad(self, task_id):
        url = f"{BONITA_URL}/API/bpm/userTask/{task_id}/execution"
        response = self.session.post(url, json={})
        return response.status_code == 204
    

    def obtener_tarea_pendiente(self, case_id):
        """
        Devuelve la primer tarea pendiente a partir de un case_id.
        """

        # Prepara los datos para hacer la petición.
        url = f"{self.base_url}/API/bpm/userTask"
        params = {
            'caseId': case_id, 
            'state': 'ready'
        }
        headers = {
            'X-Bonita-API-Token': self.csrf_token
        }

        # Realiza la petición.
        response = self.session.get(url, headers=headers, params=params)

        # Levanta una excepción para los errores 4xx y 5xx.
        response.raise_for_status()

        # Verifica si hay tareas pendientes o no, en caso afirmativo devuelve el ID de la primera.
        if not response.json():
            return None
        return response.json()[0]['id']


    def completar_tarea(self, task_id):
        """
        Completa la tarea recibida por parámetro.
        """

        # Prepara los datos para la petición.
        url = f"{self.base_url}/API/bpm/userTask/{task_id}/execution"
        headers = {
            'X-Bonita-API-Token': self.csrf_token,
            'Content-Type': 'application/json'
        }
        params = {
            "assign": "true"
        }

        # Realiza la petición.
        response = self.session.post(url, headers=headers, params=params, json={})
    
        # Levanta una excepción para los errores 4xx y 5xx.
        response.raise_for_status()

        # Retorna la respuesta.
        if response.status_code == 204 or not response.text:
            return {"message": "Tarea completada correctamente"}
        return response.json()