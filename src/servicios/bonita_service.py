import requests

BONITA_URL = "http://localhost:8080/bonita/"
password = 'bpm'
user = 'walter.bates'

class BonitaService:
    def __init__(self):
        self.session = self.bonita_login(BONITA_URL, user, password)
       
    

    def bonita_login(base_url: str, username: str, password: str):
        """
        Se conecta al loginservice de Bonita y devuelve una sesión de requests 
        con las cookies de autenticación.
        """
        LOGIN_URL = f"{base_url}/loginservice"
        login_data = {
            'username': username,
            'password': password,
            'redirect': 'false'
        }
        session = requests.Session()
        try:
            response = session.post(
                LOGIN_URL,
                data=login_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            response.raise_for_status()
            if response.status_code == 200:
                token = session.cookies.get('X-Bonita-API-Token')
                print(f"X-Bonita-API-Token obtenido: {token}")
                return session
        except HTTPError as http_err:
            print(f"Error HTTP al conectarse a Bonita: {http_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"No se puede conectar al servidor de Bonita: {req_err}")
            return None

    
    def iniciar_proceso(self, process_id):
        url = f"{BONITA_URL}/API/bpm/process/{process_id}/instantiation"
        response = self.session.post(url, json={})
        return response.json()
    

    def completar_actividad(self, task_id):
        url = f"{BONITA_URL}/API/bpm/userTask/{task_id}/execution"
        response = self.session.post(url, json={})
        return response.status_code == 204