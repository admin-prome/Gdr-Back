import json, requests, re, os, logging
import time
import traceback
from jira import JIRA
from flask import jsonify, request
from source.modules.filesTools import borrarDirectorio
#from source.jiraModule.components.getAllProjects.model_GDR import JiraUsersId, NominaUsersIds
from source.modules.getUserIdForJIRA.controller_getUserIdForJIRA import getIdJiraUser
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
from source.modules.sendMail.enviarCorreo import *
from werkzeug.utils import secure_filename
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import cast, String
from source.modules.timeTools.time import *
jiraServices = JiraService()
conexion = Conexion()
ENVIROMENT: str = settings.ENVIROMENT
domain: str = settings.DOMAIN
mail: str = settings.MAIL
tokenId: str = settings.APIKEY
print(ENVIROMENT, domain, mail, tokenId)





def waitUntilClosed(path:str) -> None:
    while os.path.isfile(path):
        timeout: int = 60
        start_time = time.time()
        while True:
            try:
                with open(path, 'r'):
                    pass  # Intenta abrir el archivo en modo lectura (si se puede abrir, está desbloqueado)
                    os.remove(path)
                    
            except PermissionError as e:
                print('Error de permisos', e)
                pass  # Si hay un error de permisos, el archivo está bloqueado por otro proceso
            
            except Exception as e:
                print('-----------')
                print(e)
            
            if time.time() - start_time >= timeout:
                return False  # Se alcanzó el tiempo máximo de espera


def updateValueDb(categoria: str, subcategoria: str = None):
    """
    Actualiza el valor en la base de datos y devuelve el valor actualizado.

    Args:
        categoria (str): Categoría.
        subcategoria (str, opcional): Subcategoría.

    Returns:
        int: Valor actualizado.
    """
    numerador = None

    try:
        query = db.session.query(Numerador).filter(
            Numerador.categoria == categoria,
            Numerador.subcategoria == subcategoria if subcategoria is not None else Numerador.subcategoria.is_(None)
        )

        numerador = query.first()

        if numerador:
            numerador.valor += 1
            db.session.commit()

    except Exception as e:
        db.session.rollback()
        print(f'Ocurrió un error al actualizar el valor en la base de datos: {e}')

    return numerador.valor if numerador else None


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
    Pre:
    Pos: comforma un diccionario con las iniciativas de la tabla GDR
    '''

    idNumbers: dict = {}
    idNumber: dict = {'category': str, 'subcategory': str, 'value' : int}
    consulta: Numerador = None
    valorActualizado: int = 0
    
    try:
        #Actualizo el valor en la BD
        if category == 'FIX':
            valorActualizado = updateValueDb(category) 
        else:
            valorActualizado = updateValueDb(category, subcategory)   
        
        #Obtengo la tabla como un objeto Numerador    
        consulta = db.session.query(Numerador)        
        resultados = consulta.all()
      
        #Obtengo el ultimo valor 
        #valor = getValue(category, subcategory, resultados)
        db.session.commit()
        
        
    except Exception as e:
        db.session.rollback()
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

        if dataIssue['issuetype'] == "FIX":
            issueDict["project"] = "GDD"
            dataIssue["key"] = "GDD"
        else:
            if dataIssue["issuetype"] == "INF":
                issueDict["project"] = "GT"
                dataIssue["key"] = "GT"
                issueDict["priority"] = {"id": '3'}
            elif dataIssue["issuetype"] == 'INC':
                issueDict["project"] = "GGDI"
                dataIssue["key"] = "GGDI"
            else:
                issueDict["project"] = "GDD"
                dataIssue["key"] = "GDD"
                issueDict["priority"] = {"id": '3'}

        return str(dataIssue['key'])

    except Exception as e:
        print(f'Ocurrió un error al mapear proyecto: {e}')


def mapearCamposParaJIRA(issue: Issue, issueDict: dict, idUltimoRequerimiento: str | list) -> None:
    """ Mapeo de campos mínimos de JIRA

    Args:
        issue (Issue): Objeto de Issue con los datos.
        issueDict (dict): Datos formateados para enviar a JIRA.
        idUltimoRequerimiento (str | list): ID del último requerimiento encontrado.
    """

    print('------------- Mapeando campos para JIRA ------------------')
    
    try:
        if '"' in issue.summary or "'" in issue.summary:
            issue.summary = issue.summary.replace('"', ' ').replace("'", ' ')

        if issue.summary == "FIX":
            tituloDelRequerimiento = f'[{issue.issuetype}-{issue.subissuetype}] {issue.summary}'
        else:
            tituloDelRequerimiento = f'[{issue.issuetype}-{issue.subissuetype} {str(idUltimoRequerimiento).zfill(3)}] {issue.summary}'

        issueDict['summary'] = tituloDelRequerimiento
        issue.summary = tituloDelRequerimiento

        description = f"""
            *Fecha de Creación:* {str(obtenerFechaHoraBsAs())}
            *Creado por:* {issue.userCredential.name}
            *Correo:* {issue.userCredential.email}
            *Rol:* {issue.managment}
            *Funcionalidad:* {issue.description}
            *Beneficio:* {issue.impact}
            *Enlace a la Documentación:* {issue.attached}.
            *Prioridad* definida por el usuario: {issue.priority}
        """
        issueDict["description"] = description

    except Exception as e:
        print(f'Ocurrió un error en el mapeo de issueDict: {e}')
        enviarCorreoDeError('Ocurrió un error en el mapeo de issueDict', str(e))


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
        status = '201'
        response = {"link": link, "status": status, "issue": issueDict}

    except Exception as e:
        print(f"Ocurrió un error al mapear la respuesta: {e}")
        dataIssue['link'] = link
        enviarCorreoDeError(issueDict.get('summary', ''), str(e))

    return response


def attachFiles(data: request, newIssue, jiraServices):
    
    try:
        print('Comienzo adjuntar arhivos')
        if data.files['myFile']:
            print('Se encontro un archivo para adjuntar')
            print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
            print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')        
            cwd = os.getcwd()  # Get the current working directory (cwd)
            if not os.path.exists(f'{cwd}/docs/tmpFilesReceived/'):
                os.mkdir(f'{cwd}/docs/tmpFilesReceived/')
        
            files = os.listdir(cwd)  # Get all the files in that directory
            #print("Files in %r: %s" % (cwd, files))
            print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
            print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-')
            
            archivo_adjunto = data.files['myFile']
            
            # Obtén el nombre de archivo original de manera segura
            nombre_archivo_original = secure_filename(archivo_adjunto.filename)
            
            # Genera un timestamp con formato año-mes-día-hora-minuto-segundo
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')          
            
            # Construye el nombre del archivo de salida con la extensión original
            nombre_archivo_salida = f'{timestamp}_{nombre_archivo_original}'
            
            # Guarda el archivo con el nombre de archivo de salida
            archivo_adjunto.save(f'docs/tmpFilesReceived/{nombre_archivo_salida}')
            
            #files = {"file": (archivo_adjunto.filename, open(f'docs/tmpFilesReceived/{nombre_archivo_salida}',"rb"), "application-type")}
            
            # Ruta completa del archivo que deseas adjuntar
            ruta_archivo_adjunto = f'docs/tmpFilesReceived/{nombre_archivo_salida}'

            # Nombre que deseas dar al archivo adjunto
            nombre_archivo = nombre_archivo_salida
            print('Adjuntando archivo')
            
            # Adjunta el archivo al problema (issue) recién creado
            jiraServices.add_attachment(issue=newIssue, attachment=ruta_archivo_adjunto, filename=nombre_archivo)
            borrarDirectorio.clear_directory(ruta_archivo_adjunto)
        
        else: print(f'No se encontraron archivos para adjuntar')
        
    except Exception as e:
        print(f'Ocurrio un error, No se encontraron archivos para adjuntar: {e}')


def enviarCorreoRequerimientoCreado(status, issue, issue_dict, data_issue, id_ultimo_requerimiento):
    if status == '201':
        correo_gerente = issue.approvers.email
        asunto = f'Requerimiento creado con GDR: {issue_dict["summary"]} - No responder'

        destinatarios = [data_issue['userCredential']['email']]

        if data_issue['priority'].upper() in ['ALTA', 'MUY ALTA', 'NORMATIVA']:
            destinatarios.append(correo_gerente)

        if data_issue['issuetype'] == 'INF':
            destinatarios.append('infra_tecno@provinciamicrocreditos.com')
        elif data_issue['issuetype'] == 'INC':
            destinatarios.append('gdi@provinciamicrocreditos.com')
        else: 
            destinatarios.append('analisis@provinciamicrocreditos.com')
        response = mapearRespuestaAlFront(issue, data_issue, issue_dict)
        
        enviarCorreo(destinatarios, asunto, armarCuerpoDeCorreo(data_issue, id_ultimo_requerimiento))
    else:
        data_issue['summary'] = f"ERROR al crear: {data_issue['summary']}"
        enviarCorreoDeError(data_issue['summary'], str(status))
        response = mapearRespuestaAlFront(issue, data_issue, issue_dict)


def createIssue(dataRequest: request) -> json:
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
    archivo: object = None
   
    try:
                
        print('------------- INICIANDO CREAR REQUERIMIENTO  ---------------')          
        dataIssue_str = dataRequest.form['myJson']
        dataIssue = json.loads(dataIssue_str)    
               
        print('--------------------------------------------------------------------')  
        print('-----------------------REQUERIMIENTO RECIBIDO-----------------------')   
        
        print('--------------------------------------------------------------------')
        print('--------------------------------------------------------------------')     
        logging.info(dataIssue)
        
   
        
        try:            
            print('--------------------------------------------------------------------')
            print('------------------ INICIO DE MAPEO DEL INCIDENTE -------------------')     
            issue = Issue(dataIssue)      
            issue.key = 'GDD'  
            print(f'esto es issue key: {issue.key}')
            print('--------------------------------------------------------------------')
            print('--------------------------------------------------------------------')              
            
        except Exception as e : 
            print('------------------- NO se pudo Mapear-----------------')
            print(f'Ocurrio un error al mapear el requerimiento: {e}')
            print('------------------- NO se pudo Mapear-----------------')
        
          
        ###################### Inicio del conexión con jira api ##############################
        print('------------------- Iniciando Conexión a JIRA --------------------') 
        print('Iniciando Conexión a JIRA')
        jiraOptions = {'server': "https://"+domain+".atlassian.net"}
        jira = JIRA(options=jiraOptions, basic_auth=(mail, tokenId))
        jira = jiraServices.getConection()      
        print('------------------------------------------------------------------') 
        #######################################################################################
        print('#######################################################################################')
        print('#######################################################################################')
        print('#######################################################################################')
        print(f'esto es issue key antes: {issue.key}')
        ########################## Mapeo de campos adicionales para JIRA ######################
        print('-------- Inicio de mapeo de campos adicionales para JIRA ---------') 
        print('Inicio de mapeo de campos adicionales para JIRA')
        issue.setKey(clasificarProyecto(dataIssue, issueDict))
        print(f'esto es issue key despues: {issue.key}')
        print('#######################################################################################')
        print('#######################################################################################')
        print('#######################################################################################')
        
        idUltimoRequerimiento = getNumberId(dataIssue['issuetype'], dataIssue.get('subissuetype'))    
        mapearCamposParaJIRA(issue, issueDict, str(idUltimoRequerimiento))
        MapeoDeRequerimientos(issue, issueDict, ENVIROMENT)    
        print('------------------------------------------------------------------')      
        #######################################################################################
        
        
        print('---------------- ASIGNANDO LLAVE DE TABLERO DE JIRA ----------------')        
        issueDict["project"] = issue.key
        print(f'esto es el issue.key: {issue.key}')                      
        print('--------------------------------------------------------------------')     
        
        ############################# ELIMINANDO REPORTER EN CASO #############################
        print('------------------- VERIFICANDO ELIMINACION DE REPORTER --------------------')
        if issueDict["project"] not in ('GDD', 'TSTGDR'):
            print('--------------------- ELIMINANDO REPORTER ----------------------')           
            reporter_value = issueDict.pop("reporter", None)  # Elimina "reporter" si existe, o devuelve None si no existe
            if reporter_value is not None:
                print(f"Valor eliminado de 'reporter': {reporter_value}")
            print(issueDict)
        
        #######################################################################################
        
        
        ############################ ENVIANDO REQUERIMIENTO A JIRA ############################  
        print('--------------------------------------------------------------------')

        newIssue = jira.create_issue(fields=issueDict)        
        print(f'creando requerimiento: {newIssue} \n')  
        
        print('--------------------------------------------------------------------')        
        print('--------------------------------------------------------------------')
        #######################################################################################
        
        ##############################  ADJUNTANDO ARCHIVOS EN JIRA  ##########################
        
        try:
            print('--------------------------------------------------------------------')
            print('------------------- ADJUNTANDO ARCHIVOS EN JIRA --------------------')
            attachFiles(dataRequest, newIssue, jira)        
            print('--------------------------------------------------------------------')        
            print('--------------------------------------------------------------------')    
            
        except: 
            print('No hay archivos adjuntos') 
            
        #######################################################################################    
        
             
        
        status = '201'                
        #enviarCorreoDeError(dataIssue['summary'], str(issueDict))
        
        if status == '201':         
            enviarCorreoRequerimientoCreado(status, issue, issueDict, dataIssue, idUltimoRequerimiento)
        else:
            dataIssue['summary'] = f"ERROR al crear: {dataIssue['summary']}"
            enviarCorreoDeError(dataIssue['summary'], str(status))
            
        response = mapearRespuestaAlFront(newIssue, dataIssue, issueDict)
            
        #wait_until_closed(ruta_archivo_adjunto)
        
        return jsonify(response)
    
    except requests.exceptions.HTTPError as e:
        
        response_json = e.response.json()
        error_messages = response_json.get("errorMessages", [])
        errors = response_json.get("errors", {})
        print(f"Error al crear el issue en JIRA: {error_messages} - {errors}")
        enviarCorreoDeError(issueDict.get('summary', ''), f'{error_messages} -> {errors}')
        return jsonify(response)

    except Exception as e:
        print(f"Error al crear el issue en JIRA: {e}")
        enviarCorreoDeError(issueDict.get('summary', ''), str(e))
        enviarCorreo(destinatarios, 'ERROR EN GDR: NO SE PUDO CREAR SU REQUERIMIENTO', armarCuerpoDeCorreo(dataIssue, idUltimoRequerimiento))
    
   
        print('-----------------------------')
        print(f'esto es el response: {response}')
        print('-----------------------------')
        return jsonify(response)
        
    
    #return {'link': 'http://requerimientos.provinciamicrocreditos.com/error', 'status': '400'}


