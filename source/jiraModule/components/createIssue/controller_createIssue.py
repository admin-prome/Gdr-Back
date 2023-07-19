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
    if subcategoria is None:
        numerador =  db.session.query(Numerador).filter(Numerador.categoria == categoria, Numerador.subcategoria.is_(None)).first()
    else:
        numerador = db.session.query(Numerador).filter_by(categoria=categoria, subcategoria=subcategoria).first()

    if numerador:
        numerador.valor += 1
        db.session.commit()
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
    
    try:
        #Actualizo el valor en la BD
        valorActualizado = updateValueDb(category, subcategory)   
        #Obtengo la tabla como un objeto Numerador    
        consulta = db.session.query(Numerador)        
        resultados = consulta.all()
      
        #Obtengo el ultimo valor 
        valor = getValue(category, subcategory, resultados)

    except Exception as e:
        print(e)
        idNumber = "Ocurrio un error en la consulta a la tabla GDR_Contador"

    print(f'esto es id number: {valorActualizado}')
    
    return int(valorActualizado)


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


def readIssueIds():
    with open('docs/issuesId.json', 'r') as archivo:
        contenido = archivo.read()
        datos = json.loads(contenido)
        print(datos)

    return datos


def up_json_GDR(data: dict, issueType: str, subIssueType: str, number: int):
    data[issueType][subIssueType] = number
    directory = "docs"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, "issuesId.json")
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def searchId(issueType: str, subIssueType: str):
    data = readIssueIds()

    if issueType in data and subIssueType in data[issueType]:
        data[issueType][subIssueType] += 1
    else:
        data[issueType] = {subIssueType: 1}

    up_json_GDR(data, issueType, subIssueType)

    return str(data[issueType][subIssueType]).zfill(3)


def update_counter(primary_key, secondary_key=None):
    with open("docs/issuesId.json") as json_file:
        data = json.load(json_file)

    if primary_key == "FIX":
        data[primary_key] += 1
    else:
        data[primary_key][secondary_key] += 1

    with open("docs/issuesId.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    updated_value = data[primary_key]
    if secondary_key is not None:
        updated_value = data[primary_key][secondary_key]

    return str(updated_value).zfill(3)


def revert_counter(primary_key, secondary_key=None):
    file_path = "docs/issuesId.json"
    if os.path.exists(file_path):
        with open(file_path, "r+") as json_file:
            data = json.load(json_file)

            if primary_key == "FIX":
                data[primary_key] -= 1
            else:
                data[primary_key][secondary_key] -= 1

            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.truncate()


def getlastIssueReq(num_issues=50, issueType: str = 'REQ', subIssueType: str = "", project: str = "GDD"):
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
    status = '400'
    response = {"link": link, "status": status}

    try:
        domain = "provinciamicroempresas"
        link = f'https://{domain}.atlassian.net/browse/{newIssue.key}'


        dataIssue['link'] = link
        status = '200'
        response = {"link": link, "status": status}

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

    try:
        #print(f'Esto es lo que llega del front: {dataIssue}')
        jiraOptions = {'server': "https://"+domain+".atlassian.net"}
        jira = JIRA(options=jiraOptions, basic_auth=(mail, tokenId))
        jira = jiraServices.getConection()

        clasificarProyecto(dataIssue, issueDict)

        idUltimoRequerimiento = getNumberId(dataIssue['issueType'], dataIssue.get('subIssueType'))


        print(f"Esto es el ID del ultimo requerimiento: {str(idUltimoRequerimiento).zfill(3)}")

        mapearCamposParaJIRA(dataIssue, issueDict, str(idUltimoRequerimiento))
        MapeoDeRequerimientos(dataIssue, issueDict, 'PROD')

        # Verificar si ya existe un requerimiento con el mismo summary
        existing_issues = jira.search_issues(f'summary ~ "{issueDict["summary"]}"')
        if existing_issues:
            existing_link = f'https://{domain}.atlassian.net/browse/{existing_issues[0].key}'
            response = {"link": existing_link, "status": "409"}

            # Restablecer el número anterior en issuesId.json
            if dataIssue['issueType'] != 'FIX':
                primary_key = dataIssue['issueType']
                secondary_key = dataIssue.get('subIssueType')
                decrement_counter(primary_key, secondary_key)

            return jsonify(response)

        newIssue = jira.create_issue(issueDict)

        print(f'creando requerimiento: {newIssue}')
        status = '200'

        if status == '200':
            correoGerente = mapeoMailGerente(str(mapeoDeGerente(str(dataIssue['approvers']), 'PROD')))
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
        revert_counter(dataIssue['issueType'], dataIssue.get('subIssueType'))
        response_json = e.response.json()
        error_messages = response_json.get("errorMessages", [])
        errors = response_json.get("errors", {})
        print(f"Error al crear el issue en JIRA: {error_messages} - {errors}")
        enviarCorreoDeError(issueDict.get('summary', ''), f'{error_messages} -> {errors}')

    except Exception as e:
        print(f"Error al crear el issue en JIRA: {e}")
        enviarCorreoDeError(issueDict.get('summary', ''), str(e))

    print('-----------------------------')
    print(f'esto es el response: {response}')
    print('-----------------------------')
    return jsonify(response)


def decrement_counter(primary_key, secondary_key=None):
    with open("docs/issuesId.json") as json_file:
        data = json.load(json_file)

    if primary_key == "FIX":
        data[primary_key] -= 1
    else:
        data[primary_key][secondary_key] -= 1

    with open("docs/issuesId.json", "w") as json_file:
        json.dump(data, json_file, indent=4)


