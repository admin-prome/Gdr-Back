from flask import jsonify
from source.jiraModule.components.userHandler.getUserSession.model_getUserSession import SessionModel
from source.modules.getUserIdForJIRA.controller_getUserIdForJIRA import getIdJiraUser

def getUserSession(userSession):
    try:
        # Obtén el ID de JIRA del usuario basado en el correo electrónico
        email = userSession['email']       
        idJIRA = getIdJiraUser(email)
        
        # Crea una instancia de SessionModel
        userSession = SessionModel(userSession)
      
        # Establece el ID de JIRA en la instancia de SessionModel
        userSession.setUserIdJIRA(idJIRA)
        
        print('--------------------------------------------')
        print(f'Esto es userSession con id: {userSession}')   
        print('--------------------------------------------')
        
        # Devuelve la sesión en forma de diccionario
        return userSession.getSession()
    
    except Exception as e:
        print(f'Ocurrió un error en getUserSession: {e}')
        return {'error': str(e)}
