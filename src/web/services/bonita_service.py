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


    def iniciar_proceso_con_datos(self, process_name, variables=None):
        """
        Inicia un proceso en Bonita y actualiza sus variables.
        
        Args:
            process_name (str): Nombre del proceso en Bonita
            variables (dict): Variables a inicializar {nombre: valor}
        
        Returns:
            str: case_id del proceso iniciado
        """
        # 1. Obtener ID del proceso
        process_id = self.obtener_id_proceso(process_name)
        if not process_id:
            raise Exception(f"No se encontró el proceso '{process_name}'")
        
        # 2. Iniciar el proceso
        url = f"{self.base_url}/API/bpm/process/{process_id}/instantiation"
        headers = {
            'content-type': 'application/json',
            'X-Bonita-API-Token': self.csrf_token
        }
        
        response = self.session.post(url, headers=headers, json={})
        response.raise_for_status()
        
        case_id = response.json()['caseId']
        
        # 3. Actualizar variables si existen
        if variables:
            self.actualizar_variables_caso(case_id, variables)
        
        return case_id


    def obtener_variables_caso(self, case_id):
        """
        Obtiene todas las variables de un caso específico.
         
        Args:
            case_id (str): ID del caso
            
        Returns:
            dict: Diccionario con las variables del caso
        """
        url = f"{self.base_url}/API/bpm/caseVariable"
        params = {
            'p': 0,
            'c': 100,
            'f': f'case_id={case_id}'
        }
        headers = {
            'X-Bonita-API-Token': self.csrf_token
        }
            
        response = self.session.get(url, headers=headers, params=params)
        response.raise_for_status()
            
        # Convertir lista de variables a diccionario
        variables_dict = {}
        for var in response.json():
            variables_dict[var['name']] = var['value']
        return variables_dict


    def actualizar_variables_caso(self, case_id, variables):
        """
        Actualiza las variables de un caso en Bonita.
        
        Args:
            case_id (str): ID del caso
            variables (dict): Diccionario con las variables a actualizar {nombre: valor}
        """
        headers = {
            'content-type': 'application/json',
            'X-Bonita-API-Token': self.csrf_token
        }
        
        for var_name, var_value in variables.items():
            url_variable = f"{self.base_url}/API/bpm/caseVariable/{case_id}/{var_name}"
            
            # Determinar tipo de Bonita según tipo de Python
            if isinstance(var_value, bool):
                bonita_type = "java.lang.Boolean"
            elif isinstance(var_value, int):
                bonita_type = "java.lang.Integer"
            else:
                bonita_type = "java.lang.String"
                var_value = str(var_value)
            
            payload = {
                "type": bonita_type,
                "value": var_value
            }
            
            # Enviar PUT request
            var_response = self.session.put(url_variable, headers=headers, json=payload)
            var_response.raise_for_status()
 
       
    def obtener_tarea_pendiente(self, case_id):
        """
        Devuelve la primer tarea pendiente a partir de un case_id.
        """
        url = f"{self.base_url}/API/bpm/humanTask"
        
        params = {
            'caseId': case_id,
            'state': 'ready'
        }
        headers = {
            'X-Bonita-API-Token': self.csrf_token
        }

        response = self.session.get(url, headers=headers, params=params)    
        response.raise_for_status()
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
    

    def obtener_variable_de_caso(self, case_id, variable_name):
        """
        Obtiene el valor actual de una variable de caso en Bonita.
        """
        url = f"{self.base_url}/API/bpm/caseVariable/{case_id}/{variable_name}"
        headers = {
            'X-Bonita-API-Token': self.csrf_token
        }
        response = self.session.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            try:
                return int(data.get("value"))
            except (ValueError, TypeError):
                return data.get("value")
        elif response.status_code == 404:
            return 0
        else:
            response.raise_for_status()


    def get_archive_case_variable(self, case_id, variable_name):
        """
        Obtiene el valor de una variable de un case.
        """
        url = f"{self.base_url}/API/bpm/archivedCaseVariable/{case_id}/{variable_name}"
        headers = {'X-Bonita-API-Token': self.csrf_token}
        
        try:
            response = self.session.get(url, headers=headers)
            if response.status_code == 200:
                return response.json().get('value')
            return None
        except Exception as e:
            return None


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


    def get_archived_cases(self, process_name=None):
        """
        Obtiene casos archivados (finalizados correctamente) de Bonita.
        """
    
        # Endpoint de casos archivados.
        url = f"{self.base_url}/API/bpm/archivedCase"
        headers = {'X-Bonita-API-Token': self.csrf_token}

        # Filtramos solo por los casos completados exitosamente.
        filters = ['state=completed']
        
        if process_name:
            process_id = self.obtener_id_proceso(process_name)
            if process_id:
                filters.append(f'processDefinitionId={process_id}')
        
        # El endpoint de bonita necesita parámetros.
        # p indica la página (0-indexed).
        # c indica la cantidad de resultados por página.
        # f indica los filtros.
        params = {
            'p': 0, 
            'c': 100,
            'f': '&'.join(filters)  # Une filtros con &.
        }

        # Se realiza la petición.
        try:
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            cases = response.json()
            return cases
        except Exception as e:
            return []


    def get_archived_tasks(self, case_id=None):
        """
        Obtiene tareas archivadas (completadas) de Bonita.
        """
        url = f"{self.base_url}/API/bpm/archivedHumanTask"
        headers = {'X-Bonita-API-Token': self.csrf_token}
        
        params = {'p': 0, 'c': 100}
        if case_id:
            params['f'] = f'caseId={case_id}'
        try:
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return []