from flask import Blueprint, request, jsonify

from source.jiraModule.components.userHandler.getUserSession.controller_getUserSession import getUserSession

getUserSession_bp = Blueprint("getUserSession_bp", __name__)

@getUserSession_bp.route('/users/getsession', methods=['POST'])
def getSession():
    try:
        print('Inicio de getSession')
        print(request)
        userCredential = request.json  # Obtener los datos del cuerpo de la solicitud JSON
        print('esto')
        print(userCredential)
        print('sdsdas')
        
        session = getUserSession(userCredential)
        # session = session
        print('--------------- Datos de la sesion inciada ------------')
        print(session)
        
        return jsonify(session)
    
    except Exception as e:
        # Manejo de excepciones
        error_message = str(e)
        return jsonify({'error': error_message}), 500  # Devuelve un error 500 (Internal Server Error)
