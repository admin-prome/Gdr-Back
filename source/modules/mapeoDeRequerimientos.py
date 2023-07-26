import json
from source.jiraModule.components.createIssue.model_createIssue import Issue
from source.modules.mapeoGerencia import *

def MapeoDeRequerimientos(issue: Issue, issue_dict : dict, ENVIROMENT: str) -> dict:
   
    names: list = ['GDD', 'GT', 'GP0007', 'RDG', 'SP000BN']
    try:
        print(f'Comienza "mapeoDeRequerimiento()": {issue.summary}')
        
        if (ENVIROMENT == 'PROD'):
            
            print(f'esto es el issue.key: {issue.key}')
            
            #MAPEO DE CAMPOS EN PROYECTO GESTIÓN DE LA DEMANDA
            if (issue.key == 'GDD'):
            
                issue_dict["customfield_10003"] = [{'accountId':str(issue.approvers.value)}]     
                        
                issue_dict["customfield_10054"] = [{'id':mapeoGerencia(issue)}]
                
                issue_dict["issuetype"] = {"id":"10001"}                         

                if((issue.finalDate != 'None') and (issue.finalDate != '')):
                    issue_dict['customfield_10038']= str((issue.finalDate[0:10]))

                if((issue.normativeDate != 'None') and (issue.normativeDate != '')):
                    issue_dict['customfield_10039']=str((issue.normativeDate[0:10]))  

            #MAPEO DE CAMPOS EN PROYECTO GESTIÓN DE TECNOLOGÍA
            elif (issue.key == 'GT'):

                issue_dict["issuetype"] = {"id":"10003"} 
                
                issue_dict['description'] = f"""{issue_dict['description']} 
                                                *Aprobado por:* {issue.approvers.name}
                                                *Gerencia:* {issue.approvers.management}"""

                if((issue.finalDate != 'None') and (issue.finalDate != ' ')):
                    issue_dict['description'] = issue_dict['description'] + '\n'  + '*Fecha de implementación:* '+ str(issue.finalDate[0:10])     
                
                if((issue.normativeDate != 'None') and (issue.normativeDate != ' ')):
                    issue_dict['description'] = issue_dict['description'] + '\n' + '*Fecha normativa:* '+ str(issue.normativeDate[0:10])               


            else:
                
                if issue.key == 'GGDI':
                    issue_dict["issuetype"] = {"id":"10090"} 
                    # issue_dict["status"] =  { "id": "10199"}
                    # print("----------------------")
                    # print(issue_dict["issuetype"] )
                    # print("----------------------")
                
                issue_dict['description'] = f"""{issue_dict['description']} 
                                                *Aprobado por:* {issue.approvers.name}
                                                *Gerencia:* {issue.approvers.management}"""

                if((issue.finalDate != 'None') and (issue.finalDate != ' ')):
                    issue_dict['description'] = issue_dict['description'] + '\n'  + '*Fecha de implementación:* '+ str(issue.finalDate[0:10])     
                
                if((issue.normativeDate != 'None') and (issue.normativeDate != ' ')):
                    issue_dict['description'] = issue_dict['description'] + '\n' + '*Fecha normativa:* '+ str(issue.normativeDate[0:10])   
        
        
        
        else:
            issue_dict["customfield_10050"] = [{'accountId': str(issue.approvers.value)}]
            
            issue_dict["customfield_10055"] = {'id': mapeoGerencia(issue)}    
                            
            issue_dict["issuetype"] = {"id":"10009"}      

            if((issue.finalDate != None) and (issue.finalDate != '')):
                issue_dict['customfield_10061']= str(issue.finalDate[0:10])

            if((issue.normativeDate != None) and (issue.normativeDate != '')):
                issue_dict['customfield_10062']= str((issue.normativeDate)[0:10])
    
    except Exception as e: 
        print(f'No se pudo mapear el requerimiento: {e}')
        
    return issue_dict