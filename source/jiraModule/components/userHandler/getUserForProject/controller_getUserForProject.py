# from source.settings.settings import settings
# from source.jiraModule.utils.conexion.conexion import Conexion
# from source.jiraModule.utils.conexion.jiraConectionServices import JiraService

# def getUsersByProject(project_key):
#     # Inicializar conexión con Jira
    
#     jiraConectionService = JiraService()
#     jiraService = jiraConectionService.getConection()

#     # # Obtener el proyecto por clave
#     # project = jiraService.project(project_key)

#     # # Obtener los usuarios asociados al proyecto
#     # users = []
#     # for role in project.roles:
#     #     if role.name == 'Developers':
#     #         users.extend(role.actors)

#     # # Formatear los usuarios y retornarlos
#     # users_formatted = [user.displayName for user in users]
#     # return users_formatted

#      # Obtener el proyecto por clave
#     project = jiraService.project(project_key)

#     # Obtener los usuarios asociados al proyecto
#     users = []
#     for role in project.roles:
#         users.extend(role.actors)

#     # Formatear los usuarios y retornarlos
#     users_formatted = [user.displayName for user in users]
#     return users_formatted