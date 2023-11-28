
import json
import re
from flask import jsonify
from source.jiraModule.utils.conexion.conexion import Conexion
import requests

# def getLatestIssuesForProject(project_key) -> json:
#     conexion = Conexion()
#     # Realizar la solicitud para buscar los issues del proyecto
#     response = conexion.get(f'search?jql=project={project_key}&maxResults=20&orderBy=created%20desc&fields=id')
#     data = response.json()
    
#     # Imprimir los resultados
#     print(json.dumps(data, sort_keys=True, indent=4, separators=(",", ": ")))
    
#     return jsonify(data)
#prueba

import requests
import unicodedata

def extract_fields_from_description(description):
    if not description:
        return {}

    fields_dict = {}

    # Definir las llaves y delimitadores para extraer los campos
    keys_and_delimiters = {
        'Creado por': 'Correo',
        'Correo' : 'Rol',
        'Rol': 'Funcionalidad',
        'Funcionalidad': 'Beneficio',
        'Beneficio': 'Enlace a la Documentación',
        'Enlace a la Documentación': 'Prioridad  definida por el usuario',
        'Prioridad  definida por el usuario': 'Iniciativa',
        'Iniciativa' : ':' 
        # Agrega más llaves y delimitadores si es necesario
    }

    # Extraer los campos usando los delimitadores definidos
    start_index = 0
    for key, delimiter in keys_and_delimiters.items():
        start_index = description.find(key, start_index)
        if start_index == -1:
            break

        start_index += len(key) + 1  # +1 para omitir el espacio después de la llave
        end_index = description.find(delimiter, start_index)
        if end_index == -1:
            fields_dict[key] = description[start_index:].strip()
            break

        fields_dict[key] = description[start_index:end_index].strip()
        start_index = end_index
    print(fields_dict)
    return fields_dict



def getLatestIssuesForProjectII(project_key):
    conexion = Conexion()

    # Realizar la solicitud para buscar los issues del proyecto con campos específicos (summary y description)
    response = conexion.get(f'search?jql=project={project_key}&maxResults=20&orderBy=created%20desc&fields=id,summary,priority,description&expand=none')
    data = response.json()

    # Función para procesar la descripción y eliminar las marcas (marks) y decodificar caracteres Unicode
    def process_description(description):
        if description is None:
            return ""

        content_blocks = description.get("content", [])

        def get_text(block):
            return block.get("text", "")

        processed_text = ""
        for block in content_blocks:
            if block["type"] == "paragraph" and "content" in block:
                paragraph_text = " ".join([get_text(content) for content in block["content"] if content["type"] == "text"])
                processed_text += unicodedata.normalize('NFKD', paragraph_text) + "\n"

        return processed_text.strip()

    # Obtener la lista de issues (requerimientos) de la respuesta
    issues = data.get('issues', [])

    # Lista para almacenar los datos de resumen y descripción de cada requerimiento
    result = []

    # Iterar sobre cada requerimiento para obtener el resumen y la descripción sin las marcas y con caracteres Unicode decodificados
    for issue in issues:
        issue_data = {
            'summary': unicodedata.normalize('NFKD', issue['fields']['summary']),
            'description': process_description(issue['fields']['description']),
            'priority': issue['fields']['priority']['name'], # Aquí obtenemos el nombre de la prioridad
            
        }
        result.append(issue_data)
    descripciones = []
    
    for issue in result:
        descripciones.append(extract_fields_from_description(issue['description']))
    print(descripciones)
        
    
    # Imprimir los resultados (opcional, para fines de depuración)
    print(json.dumps(result, sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False))

    # Devolver los datos como respuesta JSON
    return jsonify(result)

def procesar_json(json_data):
    results = []

    if json_data and isinstance(json_data, dict) and 'issues' in json_data:
        for issue in json_data['issues']:
            try:
                approver_info = issue['fields'].get('customfield_10003', [{}])[0]
                approver_display_name = approver_info.get('displayName', 'no definido')

                issue_data = {
                    'id': issue.get('id', 'no definido'),
                    'key': issue.get('key', 'no definido'),
                    'summary': issue['fields'].get('summary', 'no definido'),
                    'approver': approver_display_name,
                    'created': issue['fields'].get('created', 'no definido'),
                    'description': issue['fields'].get('description', {}).get('content', [{}])[0].get('content', [{}])[0].get('text', 'no definido'),
                    'last_updated': issue['fields'].get('updated', 'no definido'),
                    'status': issue['fields'].get('status', {}).get('name', 'no definido'),
                    'assignee': issue['fields'].get('assignee', {}).get('displayName', 'no definido')
                }
                results.append(issue_data)
            except Exception as e:
                print(f"Error al procesar el issue: {e}")

    return results





def getLatestIssuesForProject(user_email: str, maxResult: int = 10):
  
    """Obtiene todos los requerimientos que en la descripción contengan una palabra determinada."""

   
    payload = {
        "jql": f"project = {'GDD'} AND description ~ '{user_email}'",
         "expand": "summary,assignee,created,description,changelog",
         "maxResults": maxResult
    }
    conexion = Conexion()

    response = response = conexion.get(payload)
    if response.status_code == 200:
        response = response.json()
   
        respuesta = procesar_json(response)
     
        return respuesta
    else:
        raise Exception(f"Error al obtener los requerimientos: {response.status_code}")





#jql=project={project_key}&maxResults=5&orderBy=created%20desc