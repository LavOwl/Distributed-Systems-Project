import requests
from requests.exceptions import HTTPError, RequestException
import os

BONITA_URL = os.getenv("BONITA_BASE_URL", "http://localhost:8080/APIbonita").rstrip("/")
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
        if not BONITA_URL or not BONITA_USER or not BONITA_PASS:
            print("Error: BONITA_BASE_URL, BONITA_USER o BONITA_PASSWORD no están configurados.")


        LOGIN_URL = f"{BONITA_URL}/loginservice"
        login_data = {
            'username': BONITA_USER,
            'password': BONITA_PASS,
            'redirect': 'false'
        }
        self.session = requests.Session()
        try:
            response = self.session.post(
                LOGIN_URL,
                data=login_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

            print(f"Respuesta del login: {response.status_code} - {response.text}")

            print("Cookies después del login:", self.session.cookies.get_dict())

            response.raise_for_status() # Lanza un error para códigos 4xx/5xx

            token = self.session.cookies.get("X-Bonita-API-Token")
            if not token:
                return None
            self.csrf_token = token
            return self.session
        
        except (HTTPError, RequestException) as e:
            print(f"Error login Bonita: {e}")
            return False

    
    def get_process_id(self):
        url = f"{self.base_url}/API/bpm/process"
        name_process = "proceso_de_ejecucion"
        params = {
            'name': name_process
        }
        headers = {
            'X-Bonita-API-Token': self.csrf_token
        }
        response = self.session.get(url, params=params, headers=headers)
        response.raise_for_status()
        print ("Respuesta de get_process_id:", response.status_code, response.text)
        return response['id']
      
    def iniciar_proceso(self, process_id):
        print("Iniciando proceso con ID:", process_id)
        url = f"{self.base_url}/API/bpm/process/{process_id}/instantiation"
        headers = {
            'content-type' : 'application/json',
            'X-Bonita-API-Token': self.csrf_token
        }
        resp = self.session.post(url,headers= headers)
        print (f"Respuesta de iniciar proceso: {resp.status_code} - {resp.text}")
        if resp.status_code in (401, 403):
            # reintento
            if self.bonita_login():
                resp = self.session.post(url, headers= headers)
        resp.raise_for_status()
        return resp.json()

    

    def completar_actividad(self, task_id):
        url = f"{BONITA_URL}/API/bpm/userTask/{task_id}/execution"
        response = self.session.post(url, json={})
        return response.status_code == 204