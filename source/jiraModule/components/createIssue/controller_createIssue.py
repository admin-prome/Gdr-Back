import json, requests, re
from jira import JIRA
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


def getlastIssueReq(num_issues=10, issueType: str = 'REQ'):
    try:
        # Configure el servidor Jira y la autenticación
        server = f"https://{domain}.com"
        api_url = f"{server}/rest/api/2/search"
        if (issueType == 'REQ'):
            regex = r"\[REQ\s+(\d+)\]"
        elif(issueType == "INC"):
            regex = r"\[INC\s+(\d+)\]"
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
    except Exception as e:
        print(f"Ocurrió un error al obtener los últimos requerimientos: {e}")
       
    return req_ids


def createIssue(dataIssue: dict) -> json:
    link: str = ''
    newIssue: object = None
    try:
        print(f'Esto es lo que llega del front: {dataIssue}')
        dataIssue['key'] = 'GDD'
       
        

        jiraOptions ={'server': "https://"+domain+".atlassian.net"}
        jira = JIRA(options=jiraOptions, basic_auth=(mail, tokenId))
        jira = jiraServices.getConection()
        
        
        idUltimoRequerimiento: str = ''
        idUltimoRequerimiento = getlastIssueReq()    
        
        # try:
            
        #     # Convertir el valor de 'userCredential' de string a diccionario
        #     user_credential = json.loads(dataIssue['userCredential'])
        #     print(user_credential)
        #     print(type(user_credential))
        #     # Acceder a la clave 'given_name' en el diccionario 'user_credential'          

        #     user: str = user_credential['given_name']
        #     userEmail: str = user_credential['email']
            
        # except: print('fallo mapeo de google')
        
        #CAMPOS MINIMOS NECESARIOS PARA CREAR EL REQUERIMIENTO EN JIRA
        issueDict = {
                        #"project": dataIssue['key'],
                        "project": "GDD",
                        "summary": '[REQ '+ idUltimoRequerimiento+'] ' + dataIssue['summary'],
                        "description": str(f"""
                                        *Creado por:* {dataIssue['user']['name']}
                                        *Correo:* {dataIssue['user']['email']}                                        
                                        *Rol:* {dataIssue['managment']}
                                        *Funcionalidad:* {dataIssue['description']}
                                        *Beneficio:* {dataIssue['impact']}
                                        *Enlace a la Documentación:* {dataIssue['attached']}.
                                        *Prioridad* definida por el usuario: {dataIssue['priority']} 
                                        *Iniciativa:* {dataIssue['initiative']}
                                        """), #+ '\n Iniciativa: '+ dataIssue['initiative'],        
                                        
                        "priority": {"id": '3'},
                        "issuetype": {"id": "10001"}                        
                    }   
        
        MapeoDeRequerimientos(dataIssue, issueDict, 'PROD')
 
        
        for i in issueDict.keys():
            print(f'{i} : {issueDict[i]}')
            
        try:       
            #Descomentar para crear un requerimiento en JIRA            
            newIssue = jira.create_issue(issueDict)
            print(f'creando requerimiento: {newIssue}')
            #Formateo el enlace al requerimiento            
            status = '200'    
            
        except requests.exceptions.HTTPError as e:
            response_json = e.response.json()
            error_messages = response_json.get("errorMessages", [])
            errors = response_json.get("errors", {})
            print(f"Error al crear el issue en JIRA: {error_messages} - {errors}")
            status = f"Error: {error_messages}"
            
        except Exception as e:
            print(f"Error al crear el issue en JIRA: {e}")
            
        #jira.add_attachment(issue=new_issue, attachment='C:/Users/Colaborador/Documents/logo-icon.png')
       
    except Exception as e:
        print(f'Ocurrio un error en la ejecucion de crear requerimiento: {e}')    
        status = f'Error: {e}'
    
    try: 
        link = str(f'https://{domain}.atlassian.net/browse/{newIssue.key}')
        
    except: link = 'hola mundo'
    
    return jsonify({"link":link, "key":link})

  