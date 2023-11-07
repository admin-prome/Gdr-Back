from flask import jsonify
from source.jiraModule.components.userHandler.getUserSession.model_getUserSession import SessionModel
from source.modules.getUserIdForJIRA.controller_getUserIdForJIRA import getIdJiraUser
from source.modules.getDetailsUser import controller_getDetailsUser
import concurrent.futures

def get_user_details_async(email):
    user_details = controller_getDetailsUser.getUserDetails(email)
    return user_details

def getUserSession(userSession):
    try:
        print('------ Inicio de getUserSession -----')
        # Obtén el ID de JIRA del usuario basado en el correo electrónico
        email = userSession['email']
        idJIRA = getIdJiraUser(email)

        # Crea una instancia de SessionModel
        user_session = SessionModel(userSession)

        # Establece el ID de JIRA en la instancia de SessionModel
        user_session.setUserIdJIRA(idJIRA)
        print(f'esto es userSession: {user_session}')
        # Iniciar un hilo para obtener los detalles del usuario de forma paralela
        with concurrent.futures.ThreadPoolExecutor() as executor:
            user_details_future = executor.submit(get_user_details_async, email)

        user_details = user_details_future.result()

        # Agrega los detalles del usuario al diccionario user_session
        user_session.getSession()['userDetails'] = user_details

        # Devuelve la sesión en forma de diccionario
        return user_session.getSession()

    except Exception as e:
        print(f'Ocurrió un error en getUserSession: {e}')
        return {'error': str(e)}
