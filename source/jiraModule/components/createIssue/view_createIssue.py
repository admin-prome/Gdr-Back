from jira import JIRA
import requests
from source.modules.mapeoDeRequerimientos import MapeoDeRequerimientos
from source.jiraModule.utils.conexion.conexion import Conexion
from flask import Blueprint, jsonify, request
import json
from source.jiraModule.utils.conexion import conexion
from source.settings.settings import settings
from source.jiraModule.utils.conexion import jiraConectionServices
from source.jiraModule.components.createIssue import controller_createIssue



# conexion = Conexion()
createIssue_bp = Blueprint("createIssue_bp", __name__)

#Crear requerimiento con la libreria de Jira

@createIssue_bp.route('/createissue', methods=['POST'])
def CreateNewIssue() -> json:  
    try:
        print('------------------POR RESPONSE-----------------')
        response = controller_createIssue.createIssue(request)     
        print(response)
    except Exception as e:
        print(f'Ocurrio un error en la creación de la incidencia: {e}')
        
    # response.headers.add('Access-Control-Allow-Origin', '*')  # Permitir solicitudes desde cualquier origen
    # response.headers.add('Content-Type', 'application/json')  # Establecer el tipo de contenido como JSON
   
    #MAPEO DE CAMPOS PERSONALIZADOS 
    
    #jira.add_attachment(issue=new_issue, attachment='C:/Users/Colaborador/Documents/logo-icon.png')


    return response