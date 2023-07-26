
import json
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

def getLatestIssuesForProject(project_key):
    conexion = Conexion()

    # Realizar la solicitud para buscar los issues del proyecto con campos específicos (summary y description)
    response = conexion.get(f'search?jql=project={project_key}&maxResults=20&orderBy=created%20desc&fields=id,summary,description&expand=none')
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
            'description': process_description(issue['fields']['description'])
        }
        result.append(issue_data)

    # Imprimir los resultados (opcional, para fines de depuración)
    print(json.dumps(result, sort_keys=True, indent=4, separators=(",", ": "), ensure_ascii=False))

    # Devolver los datos como respuesta JSON
    return jsonify(result)




#jql=project={project_key}&maxResults=5&orderBy=created%20desc