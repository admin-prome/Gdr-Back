import json
from source.jiraModule.components.createIssue.model_createIssue import Issue
from source.modules.mapeoGerencia import *


def mapearPrioridadCliente(prioridad: str) -> str:

    print(f'Iniciando mapeo de prioridades: {prioridad}')
    prioridades: dict = {
    "Estándar" : "10070",
    "Media" : "10071",
    "Alta" : "10072",
    "Muy Alta" : "10073",
    "Normativa" : "10074" }
    print(f'cod. Prioridad: {prioridades[prioridad]}')
    return  prioridades[prioridad]


def MapeoDeRequerimientos(issue: Issue, issue_dict : dict, ENVIROMENT: str) -> dict:
    
    if ENVIROMENT == 'TST': issue.key = 'TSTGDR'
    print(f'Esto es el environment: {ENVIROMENT}')
    names: list = ['GDD', 'GT', 'GP0007', 'RDG', 'SP000BN']
    try:
        print(f'Comienza "mapeoDeRequerimiento()": {issue.summary}')
        
        
            
        print(f'esto es el issue.key: {issue.key}')
        
        #MAPEO DE CAMPOS EN PROYECTO GESTIÓN DE LA DEMANDA
        if ((issue.key == 'GDD') or (issue.key == 'FIX')):
        
            issue_dict["customfield_10003"] = [{'accountId':str(issue.approvers.value)}]     
                    
            issue_dict["customfield_10054"] = [{'id':mapeoGerencia(issue)}]
            
            issue_dict["issuetype"] = {"id":"10001"}    
              
            
            
            if (issue.isTecno == "si"):
                    issue_dict['customfield_10096'] = [{"id" :"10103"}]
            else: issue_dict['customfield_10096'] = [{"id" :"10102"}]

            if((issue.finalDate != 'None') and (issue.finalDate != '')):
                issue_dict['customfield_10038']= str((issue.finalDate[0:10]))

            if((issue.normativeDate != 'None') and (issue.normativeDate != '')):
                issue_dict['customfield_10039']=str((issue.normativeDate[0:10]))  
                
            issue_dict["reporter"] = issue.reporter
            
        #MAPEO DE CAMPOS EN PROYECTO GESTIÓN DE TECNOLOGÍA
        elif (issue.key == 'GT'):

            issue_dict["issuetype"] = {"id":"10003"} 
            
            if(issue.isTecno == 'si'): 
                issue.isTecno = 'InternoTech'
            else: issue.isTecno = 'Usuario'
            
            issue_dict['description'] = f"""{issue_dict['description']} 
                                            *Aprobado por:* {issue.approvers.name}
                                            *Gerencia:* {issue.approvers.management}
                                            *Origen:* {issue.isTecno}"""

            if((issue.finalDate != 'None') and (issue.finalDate != ' ')):
                issue_dict['description'] = issue_dict['description'] + '\n'  + '*Fecha de implementación:* '+ str(issue.finalDate[0:10])     
            
            if((issue.normativeDate != 'None') and (issue.normativeDate != ' ')):
                issue_dict['description'] = issue_dict['description'] + '\n' + '*Fecha normativa:* '+ str(issue.normativeDate[0:10])               

        
        else:
            
            if issue.key == 'GGDI':
                issue_dict["issuetype"] = {"id":"10090"} 
            
            if(issue.isTecno == 'si'): 
                issue.isTecno = 'InternoTech'                
            else: issue.isTecno = 'Usuario'
            
            if (issue.isTecno == "si"):
                    issue_dict['customfield_10096'] = [{"id" :"10103"}]
            else: issue_dict['customfield_10096'] = [{"id" :"10102"}]
            
            
            issue_dict['description'] = f"""{issue_dict['description']}                                           
                                            *Origen:* {issue.isTecno}"""
            
                # issue_dict["status"] =  { "id": "10199"}
                
            if issue.key == 'TSTGDR':
                
                if(issue.isTecno == 'si'): 
                    issue.isTecno = 'InternoTech'
                else: issue.isTecno = 'Usuario'
               
                #issue_dict["customfield_100
                issue_dict["issuetype"] = {"id":"10096"} #Tipo de requerimiento (tarea) 
                #issue_dict["reporter"] = {"accountId": "6228d7c3302c6b006af5de63","accountType": "atlassian"} #Reportado por:                   
                issue_dict["customfield_10083"] = f'{issue.userCredential.name} - {issue.userCredential.email}' #Creado por (nombre - correo)
                #issue_dict["assignee"] = {"accountId": "712020:faf61986-8ac1-47e7-9c28-8dac9ad497b8"} #Responsable de la tarea
                #issue_dict["creator"] = {"accountId": "712020:faf61986-8ac1-47e7-9c28-8dac9ad497b8","accountType": "atlassian"}
                issue_dict["customfield_10003"] = [{"accountId": issue.approvers.value, "accountType": "atlassian"}]
                issue_dict["customfield_10088"] =  issue.attached #Enlace a la documentación
                issue_dict["customfield_10089"] = issue.managment #Rol
                issue_dict["customfield_10090"] = issue.description #Funcionalidad
                issue_dict["customfield_10091"] = issue.impact #Beneficio
               
                #issue_dict["customfield_10093"] = [{"accountId": "631610a08d88ec800fbf513e","accountType": "atlassian"}] #                
                issue_dict["customfield_10084"] = {"id" : mapearPrioridadCliente(issue.priority)} #Prioridad del cliente
                issue_dict["reporter"] = issue.reporter
                
            issue_dict['description'] = f"""{issue_dict['description']} 
                                            *Aprobado por:* {issue.approvers.name}
                                            *Gerencia:* {issue.approvers.management}
                                            *Origen:* {issue.isTecno}"""

            if((issue.finalDate != 'None') and (issue.finalDate != ' ')):
                issue_dict['description'] = issue_dict['description'] + '\n'  + '*Fecha de implementación:* '+ str(issue.finalDate[0:10])     
            
            if((issue.normativeDate != 'None') and (issue.normativeDate != ' ')):
                issue_dict['description'] = issue_dict['description'] + '\n' + '*Fecha normativa:* '+ str(issue.normativeDate[0:10])   
        
        
        
    
    except Exception as e: 
        print(f'No se pudo mapear el requerimiento: {e}')
        
    return issue_dict