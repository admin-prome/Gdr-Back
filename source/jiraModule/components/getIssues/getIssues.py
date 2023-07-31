from jira import JIRA
import requests
from source.modules.generarJSON import generate_and_save_json
from source.modules.mapeoDeRequerimientos import MapeoDeRequerimientos
from source.jiraModule.utils.conexion.conexion import Conexion
from flask import Blueprint, jsonify
import json
from source.jiraModule.utils.conexion import conexion
import requests
from source.settings.settings import settings

ENVIROMENT: str = settings.ENVIROMENT
domain: str = settings.DOMAIN
mail: str = settings.MAIL
tokenId: str = settings.APIKEY

conexion = Conexion()
getIssues_bp = Blueprint("getIssues_bp", __name__)


def extraer_elementos(lista_original):
    nueva_lista = []
    for elemento in lista_original:
        nuevo_elemento = {
            "id": elemento["id"],
            "key": elemento["key"],
            "name": elemento["name"]
        }
        nueva_lista.append(nuevo_elemento)
    return nueva_lista

import requests

def get_project_fields(project_key, base_url, auth):
    project_url = f"{base_url}/rest/api/2/project/{project_key}"
    field_url = f"{base_url}/rest/api/2/field"
    
    # Obtener la configuración del proyecto
    response_project = requests.get(project_url, auth=auth)
    project_data = response_project.json()
    
    # Obtener la lista de campos personalizados
    response_fields = requests.get(field_url, auth=auth)
    fields_data = response_fields.json()
    
    # Construir una representación de los campos disponibles en el proyecto
    project_fields = []
    
    # Agregar campos predefinidos del proyecto (por ejemplo, summary, description, etc.)
    predefined_fields = ["summary", "description"]  # Agrega aquí los campos predefinidos que desees
    project_fields.extend(predefined_fields)
    
    # Agregar campos personalizados asociados al proyecto
    for field in fields_data:
        if field.get("contexts", {}).get("project", {}).get("id") == project_data["id"]:
            project_fields.append(field["name"])
    
    return project_fields

# Ejemplo de uso
base_url = "https://your-jira-instance.atlassian.net"
auth = ("username", "api_key_or_password")
project_key = "YOUR_PROJECT_KEY"

fields = get_project_fields(project_key, base_url, auth)
print(fields)


@getIssues_bp.route('/getissues', methods=['GET'])
def GetIssuesInformation() -> json:   
        
        # This code sample uses the 'requests' library:
        # http://docs.python-requests.org
        import requests
        from requests.auth import HTTPBasicAuth
        import json

        url = f"https://{domain}.atlassian.net/rest/api/2/project"

        auth = HTTPBasicAuth(mail, tokenId)

        headers = {
        "Accept": "application/json"
        }

        response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
        )
        data = response
        data = data.json()
        # print(type(json.dumps(response)))
        data = extraer_elementos(data)
        
        #email: list = []
        projectId: str = ''
        dato: list = []
        for project in data:
                projectId = project['id']
                print(projectId)
                base_url = f"https://{domain}.atlassian.net/"
                get_project_fields(projectId, base_url, auth)
                
                # url = f"https://{domain}.atlassian.net/rest/api/2/project/{projectId}"
                # response = requests.request(
                # "GET",
                # url,
                # headers=headers,
                # auth=auth
                # )
                print(response.json())
        
        # hola = requests.request(
        #         "GET",
        #         url,
        #         headers=headers,
        #         auth=auth
        #         )
         
        # mail = hola.json()
        
        # email.append(mail)
        
        # print(email)
        #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
                        
        #data = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
        
        generate_and_save_json(data, 'allProjects.json')
        
        
        
        return data