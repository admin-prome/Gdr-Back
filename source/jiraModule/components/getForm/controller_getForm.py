#from source.jiraModule.components.getForm.model_getForm import Formulario
import pprint
from source.jiraModule.components.getForm.forms_getForm import *
from flask import jsonify, request

def assignRole(email: str) -> str:    
    '''
    Pre: Recibe el email de un usuario
    Pos: Devuelve el Rol del mismo, en este caso asociado al area al cual pertenece o rol "usuario" si no pertenece a ninguno.
    '''
    
    tecnologia: list=   [ 
                            "mmillan@provinciamicrocreditos.com",
                            "jluduena@provinciamicrocreditos.com",
                            "amoragues@provinciamicrocreditos.com",
                            "mbarreto@provinciamicrocreditos.com",
                            "aescubilla@provinciamicrocreditos.com",
                            "mmoralez@provinciamicrocreditos.com",
                            "jcanepa@provinciamicrocreditos.com",
                            "jpspagnuolo@provinciamicrocreditos.com",
                            "echura@provinciamicrocreditos.com",
                            "nrivanera@provinciamicrocreditos.com",
                            "ecorbatta@provinciamicrocreditos.com",
                            "nsuarez@provinciamicrocreditos.com",
                            "mdmarino@provinciamicrocreditos.com",
                            "samartinez@provinciamicrocreditos.com"
                                    
                        ]

    procesos: list=     [   
                            "emendoza@provinciamicrocreditos.com",
                            "crojas@provinciamicrocreditos.com",
                            "rrivas@provinciamicrocreditos.com",
                            "mdegiglio@provinciamicrocreditos.com",
                            "aallan@provinciamicrocreditos.com",
                            "jarchirino@provinciamicrocreditos.com"
                                                                 
                        ]

    soporte: list=  [   
                        "saltilio@provinciamicrocreditos.com",
                        "ldominguez@provinciamicrocreditos.com",
                        "mlopez@provinciamicrocreditos.com",
                        "gorellana@provinciamicrocreditos.com",
                        "atardito@provinciamicrocreditos.com",
                        "rtoledo@provinciamicrocreditos.com"
                    ]
    
    admins: list= ['mmillan@provinciamicrocreditos.com']
    
    roles: dict= {'tecnologia': tecnologia, 'procesos': procesos, 'soporte': soporte, 'admin': admins }
   
    for role, emails in roles.items():
        if email in emails:
            return role

    return 'usuario'
    
      
def getFormByIDAndUser(form_id, email):
    '''
    Pre: Recibe el id de un formulario y el email quien solicita
    Pos: devuelve el formulario requerido asociado al rol del usuario.
    '''
    # Primero, determina el rol del usuario a partir de su correo electrónico
    user_role = assignRole(email)
    
    # Luego, obtén los IDs de formularios permitidos para ese rol
    form_ids = getFormIDs(user_role)
   
    # Verifica si el formulario con el ID especificado está permitido para el rol del usuario
    if form_id in form_ids:
        # Devuelve el formulario correspondiente al rol del usuario
        if user_role == 'tecnologia':
            return formsTecno.get(form_id, {})
        elif user_role == 'admin':
            return formsAdmin.get(form_id, {})
        elif user_role == 'procesos':
            return formsUsuario.get(form_id, {})
        elif user_role == 'user':
            return formsUsuario.get(form_id, {})
        
        
        # Agrega más casos según los roles necesarios
    else:
        return {}  # El formulario no está permitido para el rol del usuario


def getFormIDs(role)-> list[str]:
    '''
    Pre: recibe el rol.
    Pos: devuelve una lista de los ids de los formulario asociados al rol.
    '''
        
    formularios = {
        'traditional': ['tecnologia', 'procesos', 'admin', 'user'],
        'personas': ['tecnologia', 'soporte', 'admin'],
        'form5': ['soporte', 'admin'],
    }
    # Busca los IDs de formularios permitidos para el rol
    form_ids = [form_id for form_id, roles in formularios.items() if role in roles]
    return form_ids


def getForm(dataRequest: request):
    '''
    Pre: Recibe la solicitud del front con email y el id del formulario
    Pos: Devuelve el formulario requerido para el perfil del usuario
    '''
    
    data = dataRequest.json
    
    datajson = data  
    formData =  getFormByIDAndUser(datajson['formId'], datajson['email'])
    print(datajson['formId'])
    
    return  jsonify({"formData": formData})
    
    
if __name__ == '__main__':
    
    user_email = 'mmillan@provinciamicrocreditos.com'
    form_id = 'traditional'
    formulario = getFormByIDAndUser(form_id, user_email)
    
    