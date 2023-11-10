from source.modules.stringTools.convertToUnicode import normalizarTexto
from source.modules.stringTools.searchMatch import buscarCoincidencia, find_max_similarity
from source.settings.settings import settings
from source.jiraModule.components.createIssue.model_createIssue import Issue

ENVIROMENT: str = settings.ENVIROMENT

def mapeoGerencia(issue: Issue)->str:
    
    posicion: int = 1
    gerencia: str = issue.approvers.management
    #ENVIROMENT = 'PROD'
    gerencias: dict = {
                        "Administracion y Finanzas": "10028",
                        "Red de Sucursales": "10034",
                        "Cumplimiento y Procesos": "10031",
                        "Inteligencia de Negocios y Gestion estrategica": "10036",
                        "Comercial": "10030",
                        "Personas": "10033",
                        "Tecnologia": "10029",
                        "Direccion Ejecutiva": "10029",
                        "Riesgo": "10032",
                        "Comunicacion Institucional": "10035",
                        "Investigacion y Capacitacion": "10036"
                        }

    
    if( (ENVIROMENT == 'PROD') or (ENVIROMENT == 'TST')):
        posicion = 0
   
    if gerencia in gerencias:
            idGerencia = gerencias[gerencia]       
    else: idGerencia = "10029"

       
    return idGerencia


def mapeoDeGerente(gerente:str, ENVIROMENT: str) -> str:
    
    idGerente: str = ''
    gerentes: dict = {    
        "Alejandro Daniel Bermann" : "6228d69b4160640069ca557b",#Gerencite de AFyL
        "Ariel Cosentino" : "616872d97a6be400718d74b2", #Gerente de red de Sucursales
        "Carmen Eugenia Rojas Jaramillo" : "70121:5207ec8f-c9f4-456f-9116-2699e4c2f324",#Gerenta de Compliance y Procesos
        "Emiliano Fernandez" : "615e66da289a54006a2ca1e3",
        "Gisela Elin Marino" : "61bbafde08e4e00069aef74e",#Gerenta Comercial
        "Ignacio Fernando Stella" : "I6171a81dbcb57400682d861e",#Gerente de Comunicación Institucional
        "Juan Carlos Canepa" : "5cb0e51cfb6145589296296a",#Gerente de Tecnología
        "Leandro Martin Ottone" : "6228d79dc88f10006832563",
        "Mariela Alejandra Luna" : "60b55e675fa6f1006f93d22b",#Gerenta de Riesgo 
        "Mar­ia Carolina Gomez" : "61aa6bb06d002b006b02630e",  
        "Sergio Andres Rosanovich" : "6228d870a1245000688b1065"    
        }
   

    if( (ENVIROMENT == 'PROD') or (ENVIROMENT == 'TST')):
        
        if gerente in gerentes:
            idGerente = gerentes[gerente]    
        else: idGerente = gerentes['Juan Carlos Canepa']
    
    else: idGerente =  '631610a08d88ec800fbf513e'
       
    return idGerente


def mapeoMailGerente(name: str = "Juan Carlos canepa") -> str:
    """_Mapeo De Mail del Gerente_

    Args:
        name (str, optional): _El nombre del gerente tal cual se recibe del front_. Defaults to "Juan Carlos canepa".

    Returns:
        _str_: _El correo del gerente_
    """
    mail: str = ''
    managmentMail:dict =   {
                            'Ariel Cosentino' : 'acosentino@provinciamicrocreditos.com' , #Gerencia de red de Sucursales
                            'Gisela Marino' : 'gmarino@provinciamicrocreditos.com' , #Gerencia Comercial
                            'Alejandro Bermann' : 'abermann@provinciamicrocreditos.com' , #Gerencia de AFyL
                            'Juan Carlos Canepa' :'jcanepa@provinciamicrocreditos.com' , #Gerencia de Tecnología
                            'Carmen Rojas' : 'crojas@provinciamicrocreditos.com', #Compliance y Procesos
                            'Solange Altilio' : 'saltilio@provinciamicrocreditos.com', #Investigación y Capacitación
                            'Ignacio Stella' : 'istella@provinciamicrocreditos.com' , #Comunicación Institucional
                            'Mariela Luna' : 'mluna@provinciamicrocreditos.com' #Riesgo
                            }
                 
    if name in managmentMail:
            mail = managmentMail[name]      
    else: mail = managmentMail['Juan Carlos Canepa']
    
    return mail


def clasificarGerencia(texto):
    gerencias = {
        "administracion y finanzas": "10028",
        "red de sucursales": "10034",
        "cumplimiento y procesos": "10031",
        "inteligencia de negocios y gestion estrategica": "10036",
        "comercial": "10030",
        "personas": "10033",
        "tecnologia": "10029",
        "direccion ejecutiva": "10029",
        "riesgo": "10032",
        "comunicacion institucional": "10035",
        "investigacion y capacitacion": "10036"
    }

    texto_normalizado = normalizarTexto(texto)

    for gerencia, codigo in gerencias.items():
        palabras_clave = gerencia.split()  # Dividir el nombre de la gerencia en palabras clave
        if buscarCoincidencia(texto_normalizado, palabras_clave):
            return {"gerencia": gerencia, "codigo": codigo}

    return {"gerencia": "No se encontró coincidencia", "codigo": None}


def normalize_management(management: str) -> str:
    try:
        departments = {
            "administracion y finanzas": "10028",
            "red de sucursales": "10034",
            "cumplimiento y procesos": "10031",
            "inteligencia de negocios y gestion estrategica": "10036",
            "comercial": "10030",
            "personas": "10033",
            "tecnologia": "10029",
            "direccion ejecutiva": "10029",
            "riesgo": "10032",
            "comunicacion institucional": "10035",
            "investigacion y capacitacion": "10036"
        }
        options = departments.keys()
        keywords_to_ignore = ["gerencia","Gerencías", "gcia", "gerencias", "gerenc", "gerenc"]
        result = find_max_similarity(management, options, keywords_to_ignore)
        print("Best match:", result)  
    
        return result
    
    except Exception as e:
        print(f'Ocurrio un error al intentar normalizar la gerencia: {e}')
        return None



