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
from source.modules.mapeoGerencia import mapeoDeGerente, mapeoMailGerente
from source.settings.settings import settings
from source.modules.obtenerIdRequerimiento import get_req_id
from source.jiraModule.components.createIssue.model_createIssue import Issue
from source.modules.enviarCorreo import *



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
           #print(f"Último requerimiento en el proyecto {project_code}: {last_issue.get('key')} - {last_issue.get('fields').get('summary')}")
            summary = str(last_issue.get('fields').get('summary'))
            reqId = get_req_id(summary)            
        else:
            print(f"No se encontraron requerimientos en el proyecto {project_code}.")
    else:
        print(f"Error al buscar el último requerimiento del proyecto {project_code}: {response.status_code} - {response.text}")
        
    return  reqId 


def getlastIssueReq(num_issues=10, issueType: str = 'REQ', subIssueType: str = "", project: str = "GDD"):
    """
    Pre: Recibe la cantidad cantidad maxíma de requerimientos por iteración, el prefijo y el id de proyecto
    Pos: devuelve el el numero mas grande con en el proyecto con dicho prefijo.
    """
    try:
        id: str = ''
        # Configure el servidor Jira y la autenticación
        server = f"https://{domain}.com"
        api_url = f"{server}/rest/api/2/search"
        
        # if (issueType == 'REQ'):
        #     regex = r"\[REQ\s+(\d+)\]"
            
        # elif(issueType == "INC"):
        #     regex = r"\[INC\s+(\d+)\]"
       
             
        regex = fr"\[{issueType}-{subIssueType}\s+(\d+)\]"  
        print(f'Este es el regex: {regex}')
        project_code = project
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
                        print(req_ids)
                        id = str(int(req_id)+1).zfill(3)
                        
                    else:
                        print(f"No se encontró el número de requerimiento en el campo 'summary'.")
                        req_id: int = 000
                        print('-----------------------')
                        print(str((int(req_id)+1)).zfill(3))
                        
                        print('-----------------------')
                        id = str(int(req_id)+1).zfill(3)
                    return str((int(req_id)+1)).zfill(3)
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
    correoGerente: str = ''
    
    try:
        print(f'Esto es lo que llega del front: {dataIssue}')
        dataIssue['key'] = 'GDD'

        jiraOptions ={'server': "https://"+domain+".atlassian.net"}
        jira = JIRA(options=jiraOptions, basic_auth=(mail, tokenId))
        jira = jiraServices.getConection()
        
        
        idUltimoRequerimiento: str = ''
        
        if (dataIssue['issueType'] != "FIX"):
            idUltimoRequerimiento = getlastIssueReq(issueType= dataIssue['issueType'], subIssueType= dataIssue['subIssueType'])    
     
       
        
        #CAMPOS MINIMOS NECESARIOS PARA CREAR EL REQUERIMIENTO EN JIRA
        try: 
            issueDict: dict = {}
            idUltimoRequerimiento: str = ''
        
            if (dataIssue['issueType'] == "FIX"):
                tituloDelRequerimiento: str = f"[{dataIssue['issueType']}-{dataIssue['subIssueType']}] {dataIssue['summary']}"
               
            else:
                idUltimoRequerimiento = getlastIssueReq(issueType= dataIssue['issueType'], subIssueType= dataIssue['subIssueType'])    
                tituloDelRequerimiento: str = f"[{dataIssue['issueType']}-{dataIssue['subIssueType']} {str(idUltimoRequerimiento)}] {dataIssue['summary']}"
                
            issueDict['summary'] = tituloDelRequerimiento
            dataIssue['summary'] = tituloDelRequerimiento
           
            issueDict["project"] = "GDD"            
         
            description = f"""
                *Creado por:* {dataIssue['userCredential']['name']}
                *Correo:* {dataIssue['userCredential']['email']}
                *Rol:* {dataIssue['managment']}
                *Funcionalidad:* {dataIssue['description']}
                *Beneficio:* {dataIssue['impact']}
                *Enlace a la Documentación:* {dataIssue['attached']}.
                *Prioridad* definida por el usuario: {dataIssue['priority']}
                *Iniciativa:* {dataIssue['initiative']}
                """
            
            issueDict["description"] = description            
            issueDict["priority"] = {"id": '3'}         
            issueDict["issuetype"] = {"id": "10001"} 
                     
        except Exception as e: print(f'Ocurrio un error en el mapeo de issueDict: {e}')
        enviarCorreo("mmillan@provinciamicrocreditos",f"Error en GDR", f"Error al crear: {asunto} \n {e}")
        MapeoDeRequerimientos(dataIssue, issueDict, 'PROD')
        
        correoGerente = mapeoMailGerente(str(mapeoDeGerente(str(dataIssue['approvers']), 'PROD')))
        
        
        status: int = 400
        asunto: str = str('Requerimiento creado con GDR: '+ issueDict['summary']+' - No responder' )
        destinatarios: list = ["analisis@provinciamicrocreditos.com"]
        
        destinatarios.append(dataIssue['userCredential']['email'])     
        destinatarios.append(correoGerente)   
        # for i in issueDict.keys():
        #     print(f'{i} : {issueDict[i]}')
            
        print(destinatarios)
        try:       
            #Descomentar para crear un requerimiento en JIRA            
            #newIssue = jira.create_issue(issueDict)
           
            print(f'creando requerimiento: {newIssue}')
            #Formateo el enlace al requerimiento            
            status = 400    
            
            #enviarCorreo(destinatarios,asunto,armarCuerpoDeCorreo(dataIssue, idUltimoRequerimiento))
             
        except requests.exceptions.HTTPError as e:
            response_json = e.response.json()
            error_messages = response_json.get("errorMessages", [])
            errors = response_json.get("errors", {})
            print(f"Error al crear el issue en JIRA: {error_messages} - {errors}")
            status = f"Error: {error_messages}"
            enviarCorreo("mmillan@provinciamicrocreditos",f"Error en GDR", f"Error al crear: {asunto} : {e}")
            
        except Exception as e:
            print(f"Error al crear el issue en JIRA: {e}")
            enviarCorreo("mmillan@provinciamicrocreditos",f"Error en GDR", f"Error al crear: {asunto} : {e}")
           
            
        #jira.add_attachment(issue=new_issue, attachment='C:/Users/Colaborador/Documents/logo-icon.png')
       
    except Exception as e:
        print(f'Ocurrio un error en la ejecucion de crear requerimiento: {e}')          
        status = f'Error: {e}'
        enviarCorreo("mmillan@provinciamicrocreditos",f"Error en GDR", f"Error al crear: {asunto} : {e}")
    
    try: 
        link = str(f'https://{domain}.atlassian.net/browse/{newIssue.key}')
        dataIssue['link'] = link
       
    except Exception as e: 
        link = 'http://requerimientos.provinciamicrocreditos.com/error'
        dataIssue['link'] = link
        enviarCorreo("mmillan@provinciamicrocreditos",f"Error en GDR", f"Error al crear: {asunto} : {e}")
    try:
        if (status == 200):
            enviarCorreo(destinatarios,asunto,armarCuerpoDeCorreo(dataIssue, idUltimoRequerimiento))
        
        else:              
            dataIssue['summary'] =  f"ERROR al crear: {dataIssue['summary']}"
           
            #enviarCorreo(destinatarios,f"ERROR al crear: {asunto}",armarCuerpoDeCorreo(dataIssue, idUltimoRequerimiento))
    
    except Exception as e: 
        print(f'Fallo el envio de correo {e}')
        enviarCorreo("mmillan@provinciamicrocreditos",f"Error en GDR", f"Error al crear: {asunto} \n {e}")

        
    
    return jsonify({"link":link, "status":status})

  