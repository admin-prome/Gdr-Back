import json


def mapeoGerencia(gerente:str, ENVIROMENT: str)->str:
    
    posicion: int = 1
    gerencia: str = ''

    gerencias: dict = {
                        'Ariel Cosentino' : ['10034' , '10051'], #Gerencia de red de Sucursales
                        'Gisela Marino' : ['10030', '10047'], #Gerencia Comercial
                        'Alejandro Bermann' : ['10028', '10045'], #Gerencia de AFyL
                        'Juan Carlos Canepa' : ['10029', '10046'], #Gerencia de Tecnología
                        'Carmen Rojas' : ['10031', '10048'], #Compliance y Procesos
                        'Solange Altilio' : ['10036', '10053'], #Investigación y Capacitación
                        'Ignacio Stella' : ['10035', '10050'], #Comunicación Institucional
                        'Mariela Luna' : ['10032', '10049'] #Riesgo
                     }
    
    if( ENVIROMENT == 'PROD'):
        posicion = 0
   
    if gerente in gerencias:
            gerencia = gerencias[gerente][posicion]        
    else: gerencia = gerencias['Juan Carlos Canepa'][posicion]

       
    return gerencia


def mapeoDeGerente(gerente:str, ENVIROMENT: str) -> str:
    
    idGerente: str = ''

    gerentes: dict = {  'Ariel Cosentino' : '616872d97a6be400718d74b2', #Gerente de red de Sucursales
                        'Gisela Marino' : '61bbafde08e4e00069aef74e', #Gerenta Comercial
                        'Alejandro Bermann' : '6228d69b4160640069ca557b', #Gerencite de AFyL
                        'Juan Carlos Canepa' : '5cb0e51cfb6145589296296a', #Gerente de Tecnología
                        'Carmen Rojas' : '70121:5207ec8f-c9f4-456f-9116-2699e4c2f324', #Gerenta de Compliance y Procesos
                        'Ignacio Stella' : '6171a81dbcb57400682d861e', #Gerente de Comunicación Institucional
                        'Mariela Luna' : '60b55e675fa6f1006f93d22b'} #Gerenta de Riesgo 

    if( ENVIROMENT == 'PROD'):
        
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