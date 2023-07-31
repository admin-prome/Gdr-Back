import json, requests, re, os
import traceback
from jira import JIRA
from flask import jsonify
from source.modules.mapeoDeRequerimientos import MapeoDeRequerimientos
from source.jiraModule.utils.conexion.jiraConectionServices import JiraService
from source.jiraModule.components.createIssue.model_createIssue import Numerador
from source.jiraModule.utils.conexion.conexion import Conexion
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



def updateValueDb(categoria, subcategoria):
    """_summary_

    Args:
        categoria (_type_): _description_
        subcategoria (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    try:
        numerador: Numerador = None
        if subcategoria is None:
            numerador =  db.session.query(Numerador).filter(Numerador.categoria == categoria, Numerador.subcategoria.is_(None)).first()
        else:
            numerador = db.session.query(Numerador).filter_by(categoria=categoria, subcategoria=subcategoria).first()

        if numerador:
            numerador.valor += 1
            db.session.commit()
            
    except Exception as e: 
        print(f'Ocurrio un error al actualizar valor en BD: {e}')
            
    # finally: 
    #     db.session.close()    
        
    return numerador.valor


def getValue(category: str, subcategory: str, objectList : list):
    """_summary_

    Args:
        category (str): _description_
        subcategory (str): _description_
        objectList (list): _description_

    Returns:
        _type_: _description_
    """
    for object in objectList:
        if object.categoria == category and object.subcategoria == subcategory:
            return object.valor
    return None

    
def getNumberId(category: str, subcategory: str)->int:
    '''
    Pos: comforma un diccionario con las iniciativas de la tabla GDR
    '''

    idNumbers: dict = {}
    idNumber: dict = {'category': str, 'subcategory': str, 'value' : int}
    consulta: Numerador = None
    valorActualizado: int = 0
    
    try:
        #Actualizo el valor en la BD
        valorActualizado = updateValueDb(category, subcategory)   
        
        #Obtengo la tabla como un objeto Numerador    
        consulta = db.session.query(Numerador)        
        resultados = consulta.all()
      
        #Obtengo el ultimo valor 
        #valor = getValue(category, subcategory, resultados)

    except Exception as e:
        print(e)
        idNumber = "Ocurrio un error en la consulta a la tabla GDR_Contador"
        enviarCorreoDeError(idNumber, f"error: {e} / idReq: {str(valorActualizado)}")
        
    print(f'esto es id number: {valorActualizado}')
    
    return int(valorActualizado)


def clasificarProyecto(dataIssue: dict, issueDict: dict) -> str:
    """Clasificar proyecto

    Args:
        dataIssue (dict): Datos de entrada del formulario (front)
        issueDict (dict): Datos formateados para enviar a JIRA
    """
    try: 
        print('Iniciando Clasificación de proyecto')
        if (dataIssue['issueType'] == "FIX"):
            
            issueDict["project"] = "GDD"
            dataIssue["key"] = "GDD"
            
        else:

            if (dataIssue["issueType"] == "INF"): #Mapeo el requerimiento al tablero GIT
                issueDict["project"] = "GT"
                dataIssue["key"] = "GT"
                #destinatarios = ["infra_tecno@provinciamicrocreditos.com"]
                issueDict["priority"] = {"id": '3'}

            elif ( dataIssue["issueType"] == 'INC'):
                issueDict["project"] = "GGDI"
                dataIssue["key"] = "GGDI"
                #destinatarios = ["analisis@provinciamicrocreditos.com"]

            else:
                #destinatarios = ["analisis@provinciamicrocreditos.com"]
                issueDict["project"] = "GDD"
                dataIssue["key"] = "GDD"
                issueDict["priority"] = {"id": '3'}
            
            return str(dataIssue['key'])
        
    except Exception as e:   
        print(f'Ocurrio un error al mapear proyecto: {e}')


def mapearCamposParaJIRA(issue: Issue, issueDict: dict, idUltimoRequerimiento: str|list) -> None:
    """ Mapeo de campos minimos de JIRA

    Args:
        newIssue (response): respuesta de JIRA
        dataIssue (dict): Datos de entrada del formulario (front)
        issueDict (dict): Datos formateados para enviar a JIRA
        idUltimoRequerimiento(str|list): ID del ultimo requerimiento encontrado
    """
    tituloDelRequerimiento: str = ''
    description: str = ''
    print('---------------------------------------------')
    print(issue.summary)
    try:
        
        if '"' in issue.summary:
                issue.summary= issue.summary.replace('"',' ')
        if "'" in issue.summary:
                issue.summary= issue.summary.replace("'",' ')
                
        if (issue.summary == "FIX"):
            tituloDelRequerimiento: str = f'[{issue.issueType}-{issue.subIssueType}] {issue.summary}'
        else:
            tituloDelRequerimiento = f'[{issue.issueType}-{issue.subIssueType} {str(idUltimoRequerimiento).zfill(3)}] {issue.summary}'
        
        issueDict['summary'] = tituloDelRequerimiento
        issue.summary = tituloDelRequerimiento
        
        description = f"""
            *Creado por:* {issue.userCredential.name}
            *Correo:* {issue.userCredential.email}
            *Rol:* {issue.managment}
            *Funcionalidad:* {issue.description}
            *Beneficio:* {issue.impact}
            *Enlace a la Documentación:* {issue.attached}.
            *Prioridad* definida por el usuario: {issue.priority}
            *Iniciativa:* {issue.initiative}
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
    status = '400'
    response = {"link": link, "status": status, "issue": dict}

    try:
        domain = "provinciamicroempresas"
        link = f'https://{domain}.atlassian.net/browse/{newIssue.key}'


        dataIssue['link'] = link
        status = '200'
        response = {"link": link, "status": status, "issue": issueDict}

    except Exception as e:
        print(f"Ocurrió un error al mapear la respuesta: {e}")
        dataIssue['link'] = link
        enviarCorreoDeError(issueDict.get('summary', ''), str(e))

    return response


def createIssue(dataIssue: dict) -> json:
    link = ''
    newIssue = None
    correoGerente = ''
    asunto = ''
    idUltimoRequerimiento = ''
    issueDict = {}
    destinatarios = []
    status = '400'
    response = {}
    issue: object = None

    try:
        try:
            issue = Issue(dataIssue)
            print(issue)
        except Exception as e : 
            print('------------------- NO se pudo MApear-----------------')
            print(e)
            print('------------------- NO se pudo MApear-----------------')
        print(f'Esto es lo que llega del front: {json.dumps(dataIssue, indent=4)}')
        
        jiraOptions = {'server': "https://"+domain+".atlassian.net"}
        jira = JIRA(options=jiraOptions, basic_auth=(mail, tokenId))
        jira = jiraServices.getConection()

        issue.setKey(clasificarProyecto(dataIssue, issueDict))

        idUltimoRequerimiento = getNumberId(dataIssue['issueType'], dataIssue.get('subIssueType'))


        print(f"Esto es el ID del ultimo requerimiento: {str(idUltimoRequerimiento).zfill(3)}")

        mapearCamposParaJIRA(issue, issueDict, str(idUltimoRequerimiento))
        MapeoDeRequerimientos(issue, issueDict, 'PROD')

        
        #Aca se envia el requerimiento a JIRA
        newIssue = jira.create_issue(issueDict)
        

        print(f'creando requerimiento: {newIssue}')
        status = '200'
        
        if status == '200':
            correoGerente = issue.approvers.email
            asunto = 'Requerimiento creado con GDR: ' + issueDict['summary'] + ' - No responder'

            if dataIssue['priority'].upper() in ['ALTA', 'MUY ALTA', 'NORMATIVA']:
                destinatarios.append(dataIssue['userCredential']['email'])
            else:
                destinatarios = [dataIssue['userCredential']['email']]

            destinatarios.append(correoGerente)
            response = mapearRespuestaAlFront(newIssue, dataIssue, issueDict)
            enviarCorreo(destinatarios, asunto, armarCuerpoDeCorreo(dataIssue, idUltimoRequerimiento))
        else:
            dataIssue['summary'] = f"ERROR al crear: {dataIssue['summary']}"
            enviarCorreoDeError(dataIssue['summary'], str(status))
            response = mapearRespuestaAlFront(newIssue, dataIssue, issueDict)

    except requests.exceptions.HTTPError as e:
        
        response_json = e.response.json()
        error_messages = response_json.get("errorMessages", [])
        errors = response_json.get("errors", {})
        print(f"Error al crear el issue en JIRA: {error_messages} - {errors}")
        enviarCorreoDeError(issueDict.get('summary', ''), f'{error_messages} -> {errors}')

    except Exception as e:
        print(f"Error al crear el issue en JIRA: {e}")
        enviarCorreoDeError(issueDict.get('summary', ''), str(e))
        enviarCorreo(destinatarios, 'ERROR EN GDR: NO SE PUDO CREAR SU REQUERIMIENTO', armarCuerpoDeCorreo(dataIssue, idUltimoRequerimiento))
    
   
        
    print('-----------------------------')
    print(f'esto es el response: {response}')
    print('-----------------------------')
    return jsonify(response)
    #return {'link': 'http://requerimientos.provinciamicrocreditos.com/error', 'status': '400'}


