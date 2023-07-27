import json
from source.jiraModule.utils.conexion.conexion import Conexion


def checkUserInProject(email, project_key):
    conexion = Conexion()

    # Obtener el ID del proyecto por su key
    project_id = get_project_id_by_key(project_key)

    if project_id is not None:
        # Endpoint de la API de Jira para buscar usuarios por correo electrónico en un proyecto específico
        endpoint = f"/rest/api/3/user/assignable/search"
        
        # Consultar la API de Jira para buscar el usuario por correo electrónico en el proyecto
        response = conexion._get_with_params({'query': email, 'project': project_id}, endpoint)

        if response.status_code == 200:
            users = json.loads(response.text)

            if len(users) > 0:
                # El usuario existe en el proyecto
                user = users[0]
                # Aquí puedes realizar las acciones necesarias con los datos del usuario
                return user
            else:
                # El usuario no existe en el proyecto
                return "El usuario no existe en el proyecto."
        else:
            # Ocurrió un error al consultar la API de Jira
            return "Error al consultar la API de Jira."
    else:
        # El proyecto no existe o no se pudo obtener el ID del proyecto
        return "El proyecto no existe o no se pudo obtener el ID del proyecto."


def get_project_id_by_key(project_key):
    conexion = Conexion()
    
    # Endpoint de la API de Jira para obtener información de un proyecto por su key
    endpoint = f"/rest/api/3/project/{project_key}"
    
    # Consultar la API de Jira para obtener los detalles del proyecto
    response = conexion.get(endpoint)

    if response.status_code == 200:
        project_data = json.loads(response.text)
        project_id = project_data['id']
        return project_id
    else:
        # Ocurrió un error al consultar la API de Jira
        return None

