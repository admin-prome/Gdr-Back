import json, requests, re
from flask import jsonify
from source.modules.mapeoDeRequerimientos import MapeoDeRequerimientos
from source.jiraModule.utils.conexion.jiraConectionServices import JiraService
from source.jiraModule.components.createIssue.model_createIssue import IDRequerimientos
from source.jiraModule.utils.conexion.conexion import Conexion
from source.jiraModule.utils.conexion.db import engine
from source.jiraModule.utils.conexion.db import Base
from source.jiraModule.utils.conexion import db
from sqlalchemy import desc
from source.jiraModule.utils.conexion import jiraConectionServices
from source.settings.settings import settings
from source.modules.obtenerIdRequerimiento import get_req_id
from source.jiraModule.components.createIssue.model_createIssue import Issue



jiraServices = JiraService()
conexion = Conexion()
ENVIROMENT: str = settings.ENVIROMENT
domain: str = settings.DOMAIN
mail: str = settings.MAIL
tokenId: str = settings.APIKEY


def getlastIssue():
   

    # Configure el servidor Jira y la autenticación
    server = f"https://{domain}.com"
    api_url = f"{server}/rest/api/2/search"
    reqId: str = '0000'

    # Configure el parámetro jql para buscar en el proyecto deseado
    project_code = "GDD"
    jql = f"project={project_code} ORDER BY created DESC"

    # Configure los parámetros de la solicitud GET
    params = {
        "jql": jql,
        "maxResults": 1
    }

    # Envíe la solicitud GET y maneje la respuesta
    response = conexion.get(params)
    if response.status_code == 200:
        # Analizar la respuesta JSON y obtener el último requerimiento del proyecto
        result = response.json()
        issues = result.get("issues", [])
        if issues:
            last_issue = issues[0]
            print(f"Último requerimiento en el proyecto {project_code}: {last_issue.get('key')} - {last_issue.get('fields').get('summary')}")
            summary = str(last_issue.get('fields').get('summary'))
            print('+++++++++++++++++++++++++++++++++++++++++')
            print(summary)
            print(type(summary))
            print('+++++++++++++++++++++++++++++++++++++++++')
            reqId = get_req_id(summary)            
        else:
            print(f"No se encontraron requerimientos en el proyecto {project_code}.")
    else:
        print(f"Error al buscar el último requerimiento del proyecto {project_code}: {response.status_code} - {response.text}")
        
    return  reqId 


def getlastIssueReq(num_issues=10):
    # Configure el servidor Jira y la autenticación
    server = f"https://{domain}.com"
    api_url = f"{server}/rest/api/2/search"
    regex = r"\[REQ\s+(\d+)\]"
    project_code = "GDD"
    req_ids = []
    
    # Configure los parámetros de la solicitud GET
    params = {
        "jql": f"project={project_code} ORDER BY created DESC",
        "maxResults": num_issues
    }

    # Envíe la solicitud GET y maneje la respuesta
    response = conexion.get(params)
    if response.status_code == 200:
        # Analizar la respuesta JSON y obtener los últimos 10 requerimientos del proyecto
        result = response.json()
        issues = result.get("issues", [])
        if issues:
            for issue in issues:
                summary = str(issue.get('fields').get('summary'))
                match = re.search(regex, summary)
                if match:
                    req_id = match.group(1)
                    print(f"Requerimiento encontrado: {req_id}")
                    req_ids.append(int(req_id))
                    return str(int(req_id)+1)
                else:
                    print(f"No se encontró el número de requerimiento en el campo 'summary'.")
        else:
            print(f"No se encontraron requerimientos en el proyecto {project_code}.")
    else:
        print(f"Error al buscar los últimos requerimientos del proyecto {project_code}: {response.status_code} - {response.text}")
        
    return req_ids


def createIssue(dataIssue: dict) -> json:
    
    try:
        jira = jiraServices.getConection()
        idUltimoRequerimiento: str = ''
        idUltimoRequerimiento = getlastIssueReq()    
        print(idUltimoRequerimiento)
        # newIssue: Issue = None
        # input('por crear issue')

        # # newIssue = Issue(dataIssue)
        # print('----------------------------------------------------------------')    
        # print(newIssue)        
        # print('----------------------------------------------------------------')
        
        #CAMPOS MINIMOS NECESARIOS PARA CREAR EL REQUERIMIENTO EN JIRA
        issueDict = {
                        "project": dataIssue['key'],
                        "summary": '[REQ '+ idUltimoRequerimiento+'] ' + dataIssue['summary'],
                        "description": 'Rol: '+ dataIssue['managment']+ '\n'+ 'Funcionalidad: '+dataIssue['description']
                                        +'\n'+ 'Beneficio: '+ dataIssue['impact'] + 'Enlace a la Documentación: '
                                        + dataIssue['attached'], #+ '\n Iniciativa: '+ dataIssue['initiative'],        
                        "priority": {"id":dataIssue['priority']}
                    }   
        
        MapeoDeRequerimientos(dataIssue, issueDict, jiraServices.getEnviroment())
       
        try:       
            ##Descomentar para crear un requerimiento en JIRA
            newIssue = jira.create_issue(fields=issueDict)
            print('creando requerimiento')
            
        except Exception as e:
            print(f"Error al crear el issue en JIRA: {e}")
            
        
        

        #jira.add_attachment(issue=new_issue, attachment='C:/Users/Colaborador/Documents/logo-icon.png')

       
    
    
        #Formateo el enlace al requerimiento
        link = str(f'https://{domain}.atlassian.net/browse/{newIssue.key}')
        
    except Exception as e:
        print(f'Ocurrio un error en la ejecucion de crear requerimiento: {e}')    
    
  
    return jsonify({"link":link, "key":newIssue.key})
  