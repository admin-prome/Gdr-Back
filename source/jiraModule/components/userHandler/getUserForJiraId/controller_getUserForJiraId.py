import json
from source.jiraModule.utils.conexion.conexion import Conexion



def get_user_info(username):
    
    if username != 'no definido':
        conexion = Conexion()

        # Obtener el ID del proyecto por su key
        project_id = 'GDD'

        if project_id is not None:
            # Endpoint de la API de Jira para buscar usuarios por correo electrónico en un proyecto específico
            endpoint = f"/rest/api/2/user?username={username}"
            
            # Consultar la API de Jira para buscar el usuario por correo electrónico en el proyecto
            response = conexion._get_with_params({'username': username}, endpoint)

            if response.status_code == 200:
                user_info = response.json()
                return user_info
        else:
            print(f"Error: {response.status_code}")
            return 'Error al obtener'
            
    else: 
        return 'Sin asignar'
    
    
            
            
    #api_url = f"{jira_url}/rest/api/2/user?username={username}"
    
    
