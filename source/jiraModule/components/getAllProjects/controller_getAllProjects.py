from flask import jsonify
from jira import JIRA
from source.modules.filtros import filtrarProyectos
from source.settings.settings import settings
from source.jiraModule.utils.conexion.conexion import Conexion
from source.jiraModule.utils.conexion.db import engine
from source.jiraModule.utils.conexion.db import Base
from source.jiraModule.utils.conexion import db
from source.jiraModule.components.getAllProjects.model_GDR import *

ENVIROMENT: str = settings.ENVIROMENT
domain: str = settings.DOMAIN
mail: str = settings.MAIL
tokenId: str = settings.APIKEY
conexion = Conexion()

def getApprovers() -> dict:
    try:
        approvers = {}
        consulta = db.session.query(AprobadoPor)
        resultados = consulta.all()
        
        for resultado in resultados:          
            approver = {
                "id": resultado.id,
                "email": str(resultado.email),
                "value": str(resultado.idJIRA),
                "name": str(resultado.nombre),
                "management": str(resultado.area)
            }
            approvers[resultado.id] = approver

        return approvers

    except Exception as e:
        print(e)
        error = {
            "error": True,
            "mensaje": "Error en la consulta a la tabla del campo Aprobadores",
            "descripcion": "Ocurrió un error al obtener la información de los aprobadores."
        }
        return error


    

def getInitiatives()->list:
    '''     
    Pos: comforma un diccionario con las iniciativas de la tabla GDR
    '''
        
    initiatives: dict = {}
    initiative: dict = {'name': str, 'description': str}
    
    try:
        #Base.metadata.create_all(engine)    
        consulta = db.session.query(GDR)
        
        resultados = consulta.all()
        
        for resultado in resultados:          
            initiative['name'] = str(resultado.nombre)
            initiative['description'] = str(resultado.descripcion)
            initiatives[resultado.Id] = initiative            
            initiative = {}
        
    except Exception as e:
        print(e)
        initiatives = "Ocurrio un error en la consulta a la tabla del campo Iniciativas"
    
    
    return initiatives


def getAllProjects() -> list:
    '''
    Pos: consulta los proyectos en Jira, los filtra y devuelve 
    un diccionario con los mismos.    
    '''
    #aca obtengo el token del usuario decodificando.
    
    #try:
       
    #     jiraOptions ={'server': "https://"+domain+".atlassian.net"}
    #     jira = JIRA(options=jiraOptions, basic_auth=(mail))
    #     data: list=['1']
    #     projectInfo: dict = {'name': str, 'key': str}
    #     projects: dict = {}
    #     projects = jira.projects()
    #     print('-------------------------------')
    #     print(projects)
    #     for project in projects:
    #         projectInfo['key']= (project.key)
    #         projectInfo['name']= (project.name)
            
    #         data.append(projectInfo)
    #         projectInfo = {}
    #         print(project)

    #     #data = filtrarProyectos(data)
    #     sorted(data, key=lambda name: max(list(name.values())))    
        
    #     #jsonify({"projects":data})
        
    #     for i in range(data):
    #         projects[i+1] = data[i]
    #         print(data[i])
            
    #     print('--------------------------------------------------------------')
    #     print(projects)
    #     print('--------------------------------------------------------------')
    #     # return {"key": "GDD", "name": "GDD - Gesti\u00f3n de la Demanda"}
    # except Exception as e: 
    #      print(f'OCurrio un error en la ejecución de obtener proyectos: {e}')
    
    # print(data)
    #return jsonify({"projects":data})
    return{"project": {"key": "GDD", "name": "GDD - Gesti\u00f3n de la Demanda"}}