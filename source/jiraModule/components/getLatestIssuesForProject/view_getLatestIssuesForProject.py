import json
from flask import Blueprint, jsonify, request
from source.jiraModule.components.getLatestIssuesForProject import controller_getLatestIssuesForProject
from source.modules.jsonTools.save_json import guardar_json


getLatestIssuesForProject_bp = Blueprint("getLatestIssuesForProject", __name__)

@getLatestIssuesForProject_bp.route('/getissuesforuser', methods=['POST'])
def GetProjects() -> json:   
    
    try:
        print('inicio')
        user_email = request.json.get('email')
        max_result = request.json.get('max_result')
        projects = request.json.get('projects')
        response: list =  []              
        response = controller_getLatestIssuesForProject.getLatestIssuesForProjects(user_email,  projects, max_result)
        guardar_json(response, 'respuestaAlFront.json')
        return response, 201
    
    except Exception as e:
        print(f'Ocurrio un error en la creación de la incidencia: {e}')
        return jsonify({'error':f'Ocurrio un error en la creación de la incidencia: {e}'}), 500

    
