import json
from flask import Blueprint, jsonify, request
from source.jiraModule.components.getForm import controller_getForm
#from source.modules.getUserIdForJIRA.controller_getUserIdForJIRA import getIdJiraUser

getForm_bp = Blueprint("getForm_bp", __name__)


@getForm_bp.route('/GetForm', methods=['POST'])
def getForm() -> json:  
    try:
        print('------------------Comienzo de GetForm-----------------')
        
        response = controller_getForm.getForm(request)  
        response_headers = {'Content-Type': 'application/json; charset=utf-8'}
        #Content-Type: application/json; charset=utf-8
        
    except Exception as e:
        print(f'Ocurrio un error en la busqueda del formulario: {e}')

    print('------------------Fin de GetForm-----------------')
    
    return response