import json
from flask import Blueprint, jsonify
from source.jiraModule.components.userHandler.getUserForEmail import controller_getUserForEmail


getUserForEmail_bp = Blueprint("getUserForEmail_bp", __name__)

@getUserForEmail_bp.route('/getuserforemail/<proyecto>/<email>', methods=['GET'])
def getUserForEmail(proyecto: str, email: str) -> json:   
    # initiatives: list = []
    # projects: list = []
    response: dict = {}
    try:
        response = controller_getUserForEmail.checkUserInProject(email=email, project_key=proyecto)
        # initiatives = controller_getAllProjects.getInitiatives()
        print(response)
    
        # response['projects']= projects
        # response['initiatives'] = initiatives
     
        #response = jsonify({'projects': projects})
        
        
    except Exception as e:
        print(f'OCurrio un error en la ejecución de obtener proyectos: {e}')
        
    # response.headers.add('Access-Control-Allow-Origin', '*')  # Permitir solicitudes desde cualquier origen
    # response.headers.add('Content-Type', 'application/json')  # Establecer el tipo de contenido como JSON
    
    return response