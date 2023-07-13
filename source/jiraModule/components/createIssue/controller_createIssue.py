import json, requests, re
import traceback
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




def clasificarProyecto(dataIssue: dict, issueDict: dict) -> None:  
    """Clasificar proyecto 

    Args:
        dataIssue (dict): Datos de entrada del formulario (front)
        issueDict (dict): Datos formateados para enviar a JIRA
    """
            
    if (dataIssue['issueType'] == "FIX"):
        tituloDelRequerimiento: str = f"[{dataIssue['issueType']}-{dataIssue['subIssueType']}] {dataIssue['summary']}"
        issueDict["project"] = "GDD"
        dataIssue["key"] = "GDD"
    else:                
        
        if (dataIssue["issueType"] == "INF"): #Mapeo el requerimiento al tablero GIT
            issueDict["project"] = "GT"
            dataIssue["key"] = "GT"
            destinatarios = ["infra_tecno@provinciamicrocreditos.com"]  
            issueDict["priority"] = {"id": '3'}
            
        # elif ( dataIssue["issueType"] == 'INC'):
        #     issueDict["project"] = "GGDI"
        #     dataIssue["key"] = "GGDI"
        #     destinatarios = ["analisis@provinciamicrocreditos.com"]
                 
            
        else: 
            destinatarios = ["analisis@provinciamicrocreditos.com"]        
            issueDict["project"] = "GDD"              
            dataIssue["key"] = "GDD"
            issueDict["priority"] = {"id": '3'}
                    
        
def mapearCamposParaJIRA(dataIssue: dict, issueDict: dict, idUltimoRequerimiento: str|list) -> None:
    """ Mapeo de campos minimos de JIRA

    Args:
        newIssue (response): respuesta de JIRA
        dataIssue (dict): Datos de entrada del formulario (front)
        issueDict (dict): Datos formateados para enviar a JIRA
        idUltimoRequerimiento(str|list): ID del ultimo requerimiento encontrado
    """
    
    description: str = ''
    
    try:        
        tituloDelRequerimiento = f"[{dataIssue['issueType']}-{dataIssue['subIssueType']} {str(idUltimoRequerimiento)}] {dataIssue['summary']}"     
        issueDict['summary'] = tituloDelRequerimiento
        dataIssue['summary'] = tituloDelRequerimiento        
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
                   
              
                    
    except Exception as e: 
        print(f'Ocurrio un error en el mapeo de issueDict: {e}')
        enviarCorreoDeError('Ocurrio un error en el mapeo de issueDict',  str(e))


def mapearRespuestaAlFront(newIssue, dataIssue: dict, issueDict: dict) -> dict:
    """ Mapear Respuesta para el Cliente

    Args:
        newIssue (object): _description_
        dataIssue (dict): _description_
        issueDict (dict): _description_

    Returns:
        response (dict): diccionario para el cliente contiene status y el enlace al requerimiento a la pagina de error
    """
    link = 'http://requerimientos.provinciamicrocreditos.com/error'
    status: str = '400'
    response: dict = {"link": link, "status": status}
    
    try: 
        link = str(f'https://{domain}.atlassian.net/browse/{newIssue.key}')
        
        print(link)
        
        dataIssue['link'] = link
        status = '200'
        response = {"link":link, "status":status}
    
    except Exception as e: 
        print(f"Ocurrio un error al mapear el response:  {e}")
        dataIssue['link'] = link           
        enviarCorreoDeError(issueDict['summary'],   str(e))           
        
    print('..................................................')
    print(response)
    print('..................................................')
    
    return response


def createIssue(dataIssue: dict) -> json:
    link: str = ''
    newIssue: object = None
    correoGerente: str = ''
    asunto: str = ''
    e: str = ''
    idUltimoRequerimiento: str | list = ''
    issueDict: dict = {}
    destinatarios: list = []
    status: int = '400'  
    response: dict = {}
    
    try:
        print(f'Esto es lo que llega del front: {dataIssue}')        
        jiraOptions ={'server': "https://"+domain+".atlassian.net"}
        jira = JIRA(options=jiraOptions, basic_auth=(mail, tokenId))
        jira = jiraServices.getConection()        
        
        clasificarProyecto(dataIssue, issueDict)  
        print(dataIssue['issueType'])
        idUltimoRequerimiento = getlastIssueReq(issueType= dataIssue['issueType'], subIssueType= dataIssue['subIssueType'], project= dataIssue['key'])    
        mapearCamposParaJIRA(dataIssue, issueDict, idUltimoRequerimiento)     
        MapeoDeRequerimientos(dataIssue, issueDict, 'PROD')     
           
                
        # for i in issueDict.keys():
        #     print(f'{i} : {issueDict[i]}')
        
         
        #Descomentar para crear un requerimiento en JIRA            
        newIssue = jira.create_issue(issueDict)
        
        print(f'creando requerimiento: {newIssue}')
        #Formateo el enlace al requerimiento            
        status = '200'   
        
       
        if (status =='200'):      
            correoGerente = mapeoMailGerente(str(mapeoDeGerente(str(dataIssue['approvers']), 'PROD')))        
            asunto: str = str('Requerimiento creado con GDR: '+ issueDict['summary']+' - No responder' )              
            
            if((dataIssue['priority'].upper() == 'ALTA') or (dataIssue['priority'].upper() == 'MUY ALTA') or (dataIssue['priority'].upper() == 'NORMATIVA')):
                destinatarios.append( (dataIssue['userCredential']['email']))    #Agregamos al usuario que crea el requerimiento
            
            else:
                destinatarios = (dataIssue['userCredential']['email'])
                            
            destinatarios.append(correoGerente)  #Agregamos al gerente quien aprueba la carga del requerimiento 
            response = mapearRespuestaAlFront(newIssue, dataIssue, issueDict)              
            enviarCorreo(destinatarios,asunto,armarCuerpoDeCorreo(dataIssue, idUltimoRequerimiento))
            
        else:              
            dataIssue['summary'] =  f"ERROR al crear: {dataIssue['summary']}"
            enviarCorreoDeError(dataIssue['summary'],  str(status))            
            #enviarCorreo(destinatarios,f"ERROR al crear: {asunto}",armarCuerpoDeCorreo(dataIssue, idUltimoRequerimiento))
            response = mapearRespuestaAlFront(newIssue, dataIssue, issueDict)
        
                         
    except requests.exceptions.HTTPError as e:
        response_json = e.response.json()
        error_messages = response_json.get("errorMessages", [])
        errors = response_json.get("errors", {})
        print(f"Error al crear el issue en JIRA: {error_messages} - {errors}")           
        enviarCorreoDeError(issueDict['summary'],  f'{error_messages} -> {errors}')         
        
    except Exception as e:
        print(f"Error al crear el issue en JIRA: {e}")     
        enviarCorreoDeError(issueDict['summary'],  str(e))            
    
        #jira.add_attachment(issue=new_issue, attachment='C:/Users/Colaborador/Documents/logo-icon.png')
    
    #response = mapearRespuestaAlFront(newIssue, dataIssue, issueDict)
    print('-----------------------------')
    print(f'esto es el response: {response}')
    print('-----------------------------')
    return jsonify(response)

  