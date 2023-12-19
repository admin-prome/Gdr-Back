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
        print('Comienzo de obtener aprobados por')
        approvers = {}
        
        with db.Session() as session:  # Crea una nueva sesión dentro de un contexto 'with'
            consulta = session.query(AprobadoPor)
            resultados = consulta.all()
            
            for resultado in resultados:
                approver = {
                    "id": resultado.id,
                    "email": resultado.email,
                    "value": resultado.idJIRA,
                    "name": resultado.nombre,
                    "management": resultado.area
                }
                approvers[resultado.id] = approver
            db.session.close()
        print('Fin de obtener aprobados por')
        
        return approvers

    except Exception as e:
        db.session.close()
        print(e)
        error = {
        "approvers": {
            "1": {
            "email": "abermann@provinciamicrocreditos.com",
            "id": 1,
            "management": "Administracion y Finanzas",
            "name": "Alejandro Daniel Bermann",
            "value": "6228d69b4160640069ca557b"
            },
            "2": {
            "email": "acosentino@provinciamicrocreditos.com",
            "id": 2,
            "management": "Red de Sucursales",
            "name": "Ariel Cosentino",
            "value": "616872d97a6be400718d74b2"
            },
            "3": {
            "email": "crojas@provinciamicrocreditos.com",
            "id": 3,
            "management": "Cumplimiento y Procesos",
            "name": "Carmen Eugenia Rojas Jaramillo",
            "value": "70121:5207ec8f-c9f4-456f-9116-2699e4c2f324"
            },
            "4": {
            "email": "efernandez@provinciamicrocreditos.com",
            "id": 4,
            "management": "Inteligencia de Negocios y Gestion estrategica",
            "name": "Emiliano Fernandez",
            "value": "615e66da289a54006a2ca1e3"
            },
            "5": {
            "email": "gmarino@provinciamicrocreditos.com",
            "id": 5,
            "management": "Comercial",
            "name": "Gisela Elin Marino",
            "value": "61bbafde08e4e00069aef74e"
            },
            "6": {
            "email": "istella@provinciamicrocreditos.com",
            "id": 6,
            "management": "Personas",
            "name": "Ignacio Fernando Stella",
            "value": "I6171a81dbcb57400682d861e"
            },
            "7": {
            "email": "jcanepa@provinciamicrocreditos.com",
            "id": 7,
            "management": "Tecnologia",
            "name": "Juan Carlos Canepa",
            "value": "5cb0e51cfb6145589296296a"
            },
            "8": {
            "email": "lottone@provinciamicrocreditos.com",
            "id": 8,
            "management": "Direccion Ejecutiva",
            "name": "Leandro Martin Ottone",
            "value": "6228d79dc88f10006832563"
            },
            "9": {
            "email": "mluna@provinciamicrocreditos.com",
            "id": 9,
            "management": "Riesgo",
            "name": "Mariela Alejandra Luna",
            "value": "60b55e675fa6f1006f93d22b"
            },
            "10": {
            "email": "mcgomez@provinciamicrocreditos.com",
            "id": 10,
            "management": "Comunicacion Institucional",
            "name": "Mar­ia Carolina Gomez",
            "value": "61aa6bb06d002b006b02630e"
            },
            "11": {
            "email": "srosanovich@provinciamicrocreditos.com",
            "id": 11,
            "management": "Investigacion y Capacitacion",
            "name": "Sergio Andres Rosanovich",
            "value": "6228d870a1245000688b1065"
            }
            }
        }
        return error
    
    #finally:  db.session.close()
        


    

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
        
        db.session.close()
        
    except Exception as e:
        print(e)
        db.session.close()
        initiatives = "Ocurrio un error en la consulta a la tabla del campo Iniciativas"
    
    
    return initiatives


def getSystems() -> dict:
    try:
        print('Comienzo de obtener Sistemas')
        approvers = {}
        
        with db.Session() as session:  # Crea una nueva sesión dentro de un contexto 'with'
            consulta = session.query(TechnoSystem).filter(TechnoSystem.systemStatus == 1)
            resultados = consulta.all()
            
            for resultado in resultados:
                approver = {
                    "id": resultado.id,                 
                    "systemName": resultado.systemName,
                    "code": resultado.code,
                    "systemDescription" : resultado.systemDescription
                }
                approvers[resultado.id] = approver
            db.session.close()
        print('Fin de obtener proyectos')
        
        return approvers

    except Exception as e:
        db.session.close()
        print(e)


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
    #return{"project": {"key": "GDD", "name": "GDD - Gesti\u00f3n de la Demanda"}}