import json
from source.jiraModule.utils.conexion.conexion import Conexion
from source.modules.generarJSON import generate_and_save_json
from source.jiraModule.utils.conexion.jiraConectionServices import JiraService
# from source.jiraModule.utils.conexion.conexion import Conexion
# from source.modules.generarJSON import generate_and_save_json

def getProjectsForUser():
    # Crea una instancia de la clase JIRA
    jira = JiraService().getConection()

    # Obtén el proyecto por su clave (key)
    project_key = 'GDD'
    project = jira.project(project_key)

    # Obtén los usuarios del proyecto
    users = jira.search_users(project=project)
    
    print('================================================================')
    print(json.dumps(json.loads(users.text), sort_keys=True, indent=4, separators=(",", ": ")))
    print('================================================================')

    # Imprime los usuarios
    for user in users:
        print(user.displayName)
        
    
    return users

def getProjectsForUserII(accountId):
    conexion = Conexion()
    
    #url = f'user?accountId={accountId}&expand=groups,applicationRoles'
    #url = f"group/member?accountId={accountId}"
    #url = f"user/{accountId}/projects"
    url= f'project/GDD/avatars'
    try:
        response = conexion.get(path = url)
        
        response.raise_for_status()  # Comprobar si hubo un error en la respuesta del servidor
        print('================================================================')
        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        print('================================================================')
        data = response.json()
        
        #proyectos_activos = data.get("groups").get("items")
        data = response.json()
        proyectos_activos = [proyecto.get("name") for proyecto in data]
        #proyectos_activos = [grupo.get("name") for grupo in data]
        print('############################################')
        print(proyectos_activos)
        print('############################################')
        input()
        return proyectos_activos
    except Exception as e:
        print('Ocurrió un error al obtener los proyectos activos del usuario:', e)
        return None

# Llamada a la función obtener_proyectos_activos para obtener los proyectos activos de un usuario
if __name__ == '__main__':
    usuario = 'Mario Mendez'
    api_token = "tu-api-token"
    proyectos = getProjectsForUser(usuario)
    

    if proyectos is not None:
        print("Proyectos activos del usuario:", proyectos)
    else:
        print("No se pudo obtener los proyectos activos del usuario.")
