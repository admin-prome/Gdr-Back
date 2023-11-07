from sqlalchemy import String, cast
#from source.jiraModule.components.getAllProjects.model_GDR import JiraUsersId
from source.jiraModule.utils.conexion import db
from source.modules.getUserIdForJIRA.model_getUserIdForJIRA import JiraUsersId, NominaUsersIds


def getIdJiraUser(email: str) -> str:    
    """
    Pre: Recibe un correo de usuario
    Pos: Devuelve el id de JIRA del usuario ó un string vacio si no existiese en la nomina de usuarios de tecno. 
    """
    jiraId: str = ''
    print('Iniciando consulta de id de jira')
    try:
        with db.Session() as session:
            result = session.query(JiraUsersId.idJiraUser).join(NominaUsersIds, NominaUsersIds.id == JiraUsersId.idUser).filter(cast(NominaUsersIds.email, String) == email).all()
            jiraId = result[0][0] 
            
            #db.session.close()
            print(f'Este es el id de JIRA {jiraId}')
        
    except Exception as e:
        db.session.close()
        print(f'Ocurrio un error al consultar tabla id jira: {e}')        
        return "6228d8734160640069ca5686"
    
    finally:         
        db.session.close()
    
    #'result' contiene los registros con los idJiraUser correspondientes al email dado
    
    return str(jiraId)