#from source.jiraModule.components.getForm.model_getForm import Formulario
import pprint
from source.jiraModule.components.getForm.forms_getForm import *
from flask import jsonify, request

from source.modules.mapeoGerencia import normalize_management


def assignRole(email: str) -> str:    
    '''
    Pre: Recibe el email de un usuario
    Pos: Devuelve el Rol del mismo, en este caso asociado al area al cual pertenece o rol "usuario" si no pertenece a ninguno.
    '''
    try: 
        managment = data_user['userCredential']['userDetails']['management']
        print('esto es la gerencia: ',managment)
        managment_normalize = normalize_management(managment)
        print(managment_normalize)
        
        if managment_normalize:
            role = managment_normalize
            print('El rol del usuario es: %s' %role)
            return role
        
        print('El rol del usuario es: usuario')
        return 'usuario'
    
    except Exception as e:
        print(f'Fallo la asignación de roles: {e}')
        return 'usuario'
         
        
def getFormByIDAndUser(data_user):
    '''
    Pre: Recibe el id de un formulario y el email quien solicita
    Pos: devuelve el formulario requerido asociado al rol del usuario.
    '''
    form_id: str= data_user['formId']
    email: str= data_user['email']
    # Primero, determina el rol del usuario a partir de su correo electrónico
    user_role = assignRole(email)
    print('El rol definido del usuario es: %s' %user_role)
    
    # Luego, obtén los IDs de formularios permitidos para ese rol
    forms_ids = getFormIDs(user_role)
    print('Los formularios definidos del rol son: %s' %forms_ids)
   
    # Verifica si el formulario con el ID especificado está permitido para el rol del usuario
    if form_id in forms_ids:
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
    all_department: list = [    
                                'administracion y finanzas', 
                                'red de sucursales',
                                'cumplimiento y procesos',
                                'inteligencia de negocios y gestion estrategica',
                                'comercial', 'personas',
                                'tecnologia', 'direccion ejecutiva',
                                'riesgo', 'comunicacion institucional',
                                'investigacion y capacitacion',
                                'user',
                                'admin'
                            ]
    
    formularios: dict = { 
                            'traditional': all_department,
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
    
    global data_user
    data_user = dataRequest.json          
    formData =  getFormByIDAndUser(data_user)
    
    return  jsonify({"formData": formData})
    
    
if __name__ == '__main__':
    
    user_email = 'mmillan@provinciamicrocreditos.com'
    form_id = 'traditional'
    formulario = getFormByIDAndUser(form_id, user_email)
    
    