import json
from flask import Blueprint, jsonify, request
from source.jiraModule.components.getLatestIssuesForProject import controller_getLatestIssuesForProject


getLatestIssuesForProject_bp = Blueprint("getLatestIssuesForProject", __name__)

@getLatestIssuesForProject_bp.route('/getissuesforuser', methods=['POST'])
def GetProjects() -> json:   
    
    try:
        print('inicio')
        user_email = request.json.get('email')
        max_result = request.json.get('max_result', 10)
    
        print(user_email)
        print(max_result)
        
        response = controller_getLatestIssuesForProject.getLatestIssuesForProject(user_email, max_result)
        return response, 201
    
    except Exception as e:
        print(f'Ocurrio un error en la creación de la incidencia: {e}')
        return jsonify({'error':f'Ocurrio un error en la creación de la incidencia: {e}'}), 500

    
