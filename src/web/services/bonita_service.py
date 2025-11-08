import requests
import os

BONITA_URL = os.getenv("BONITA_BASE_URL", "http://localhost:8080/bonita").rstrip("/")

class BonitaService:
    def __init__(self):
        self.base_url = BONITA_URL
        self.session = requests.Session()
        self.csrf_token = None


    def bonita_login(self, data=None):
        """
        Se conecta al loginservice de Bonita y devuelve una sesión de requests con las cookies de autenticación.
        """
        username = data.get("username")     
        password = data.get("password")
        
        if not self.base_url or not username or not password:
            raise ValueError("BONITA_URL, username o passwords no están configurados.")
    
        login_url = f"{self.base_url}/loginservice"
    
        params = {
            'username': username,
            'password': password,
            'redirect': 'false'
        }
    
        self.session = requests.Session()

        try:
            response = self.session.get(
                login_url,
                params=params,  
                allow_redirects=False
            )

            # Guarda el token.
            token = self.session.cookies.get("X-Bonita-API-Token")
            if not token:
                return False
            self.csrf_token = token
            return self.session
        except Exception as e:
            return False
    
    def obtener_info_usuario(self):
        """
        Verifica si la sesión de Bonita sigue siendo válida y devuelve información
        del usuario autenticado o lanza una excepción si no está logueado.
        """
        user_url = f"{self.base_url}/API/system/session/unusedId"

        headers = {
            "X-Bonita-API-Token": self.csrf_token
        }

        response = self.session.get(user_url, headers=headers)

        if response.status_code != 200:
            raise Exception("Sesión inválida o expirada")

        return response.json()


    def obtener_grupos_usuario(self, user_id):
        """
        Devuelve una lista de los grupos a los que pertenece el usuario.
        """
        url = f"{self.base_url}/API/identity/membership"
        params = {"f": f"user_id={user_id}"}
        headers = {"X-Bonita-API-Token": self.csrf_token}

        response = self.session.get(url, headers=headers, params=params)
        response.raise_for_status()
        memberships = response.json()

        # Cada membership tiene un "group_id", así que se debe obtener el nombre del grupo.
        grupos = []
        for membership in memberships:
            group_url = f"{self.base_url}/API/identity/group/{membership['group_id']}"
            group_resp = self.session.get(group_url, headers=headers)
            if group_resp.status_code == 200:
                grupos.append(group_resp.json()["name"])
        return grupos


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


    def iniciar_proceso(self, process_name):
        """
        Recibe un nombre de proceso, busca su ID asociado, lo inicia y retorna un case_id.
        """
        # Busca el ID asociado al proceso.
        process_id = self.obtener_id_proceso(process_name)
        if not process_id:
            raise Exception(f"No se encontró el proceso '{process_name}'")
        
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
        return response.json()['caseId']


    def establecer_variable_al_caso(self, case_id, variable_name, value, tipo="java.lang.Integer"):
        """
        Establece o actualiza el valor a una variable del caso.
        """
        url = f"{self.base_url}/API/bpm/caseVariable/{case_id}/{variable_name}"
        headers = {
            'content-type': 'application/json',
            'X-Bonita-API-Token': self.csrf_token
        }
        payload = {
            "type": tipo,
            "value": value
        }
        
        response = self.session.put(url, headers=headers, json=payload)
        response.raise_for_status()
        if response.text:
            try:
                return response.json()
            except:
                return {"success": True}
        return {"success": True}


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


    def completar_tarea(self, case_id):
        """
        Completa la tarea pendiente del case_id recibido por parámetro.
        """
        # Busca el task_id asociado a la primer tarea pendiente del case_id recibido.
        task_id = self.obtener_tarea_pendiente(case_id)
        if not task_id:
            raise Exception("No hay tarea pendiente")
        
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