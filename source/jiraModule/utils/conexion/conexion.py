import requests
from requests.auth import HTTPBasicAuth
from source.settings.settings import settings

class Conexion:
    
    def __init__(self):
        self.domain = settings.DOMAIN
        self.mail = settings.MAIL
        self.tokenId = settings.APIKEY
        self.auth = HTTPBasicAuth(self.mail, self.tokenId)
        self.headers = {"Accept": "application/json", "Content-Type": "application/json"}
        self.path = ""
        self.url = "https://{0}.atlassian.net/rest/api/3/".format(self.domain)
        self.url2 = "https://{0}.atlassian.net/rest/api/2/".format(self.domain)
       
    
    def get(self, path, param = {}):
        if isinstance(path, str):
            self.path = path
            if (param != {}):
                try:
                    response = requests.get(self.url + self.path, auth=self.auth, headers=self.headers, params = param)
                except:
                    response = requests.get(self.url2 + self.path, auth=self.auth, headers=self.headers, params = param)
               
                return response
            else:
                try:
                    response = requests.get(self.url + self.path, auth=self.auth, headers=self.headers)
                except: 
                    response = requests.get(self.url2 + self.path, auth=self.auth, headers=self.headers)
                return response
        elif isinstance(path, dict):
            return self._get_with_params(path)
        else:
            raise ValueError("Invalid path type")
    
    def _get_with_params(self, params_dict):
        try:
            response = requests.get(self.url + 'search', auth=self.auth, headers=self.headers, params=params_dict)
        except:
            response = requests.get(self.url2 + 'search', auth=self.auth, headers=self.headers, params=params_dict)
        return response
    
    
    
    def post(self, path, data):
        self.path = path
        try:
            response = requests.post(self.url + self.path, auth=self.auth, headers=self.headers, json=data)
        except: 
            response = requests.post(self.url2 + self.path, auth=self.auth, headers=self.headers, json=data)
        return response
    
    def put(self, path, data):
        self.path = path
        try:
            response = requests.put(self.url + self.path, auth=self.auth, headers=self.headers, json=data)
        except: 
            response = requests.put(self.url2 + self.path, auth=self.auth, headers=self.headers, json=data)
        return response
    
    def delete(self, path):
        self.path = path
        try:
            response = requests.delete(self.url + self.path, auth=self.auth, headers=self.headers)
        except:
            response = requests.delete(self.url2 + self.path, auth=self.auth, headers=self.headers)
        return response

    def __str__(self):
        # Crear una representación de cadena para la instancia de Conexion
        return (
            f"Conexion(domain={self.domain}, "
            f"mail={self.mail}, "
            f"tokenId={self.tokenId}, "
            f"path={self.path}, "
            f"url={self.url}, "
            f"url2={self.url2}"
            # Agrega otras propiedades si es necesario
            ")"
        )