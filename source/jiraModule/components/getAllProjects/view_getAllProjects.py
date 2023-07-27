import json
from flask import Blueprint, jsonify
from source.jiraModule.components.getAllProjects import controller_getAllProjects


getAllProjects_bp = Blueprint("getAllProjects_bp", __name__)

@getAllProjects_bp.route('/GetAllProjects', methods=['GET'])
def GetProjects() -> json:   
    # initiatives: list = []
    # projects: list = []
    approvers: dict = {}
    response: dict = {}
    try:
        approvers = controller_getAllProjects.getApprovers()
        print(type(approvers))
        #projects = controller_getAllProjects.getAllProjects()
        #initiatives = controller_getAllProjects.getInitiatives()
        #print(initiatives)
    
        #response['projects']= projects
        #response['initiatives'] = {"initiatives": "0"}
        # print(projects)
     
        response = jsonify({"approvers": approvers})
        #print(f'Esto es lo que llega del front: {json.dumps(response, indent=4)}')
        print('-----------------------------------------------')
        print(response)
        print('-----------------------------------------------')
        
    except Exception as e:
        print(f'OCurrio un error en la ejecución de obtener proyectos: {e}')
        
    # response.headers.add('Access-Control-Allow-Origin', '*')  # Permitir solicitudes desde cualquier origen
    # response.headers.add('Content-Type', 'application/json')  # Establecer el tipo de contenido como JSON
    
    return response