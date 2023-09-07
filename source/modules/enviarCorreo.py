from source.settings.settings import settings

EMAIL_REMITENTE = str(settings.EMAIL_REMITENTE)
EMAIL_PASSWORD = str(settings.EMAIL_PASSWORD)

import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def readJson():
    with open('JSON/lastData.json', 'r') as archivo:
        contenido = archivo.read()
        datos = json.loads(contenido)
    return datos

  
def mapearCuerpoDeCorreo(dataIssue: dict, idUltimoRequerimiento: str):
    
    try:
       issueDetail = str(f"""
                    <a href="{dataIssue['link']}"><h3 class="Titulo">{dataIssue['summary']}</h3></a>
                    <p><b>Proyecto: </b>Gestion de la Demanda</p>
                    <p><b>Creado por: </b>{dataIssue['userCredential']['name']}</p>
                    <p><b>Correo: </b>{dataIssue['userCredential']['email']}</p>
                    <p><b>Rol: </b>{dataIssue['managment']}</p>
                    <p><b>Funcionalidad: </b>{dataIssue['description']}</p>
                    <p><b>Beneficio: </b>{dataIssue['impact']}</p>
                    <p><b>Enlace a la Documentación: </b>{dataIssue['attached']}</p>
                    <p><b>Prioridad definida por el usuario: </b>{dataIssue['priority']}</p>  
                    """)
        #<p><b>Iniciativa: </b>{dataIssue['initiative']}</p> 

    except Exception as e: 
        print(f'Ocurrio un error al mapear cuerpo del correo: {e}')        
        issueDetail ='Ocurrio un error al mapear cuerpo del correo'
        
    return issueDetail
    
    
def armarCuerpoDeCorreo(data: dict, id: str):      
    
    body = str("""
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Nuevo Requerimiento Cerado</title>

                <style>
                body {
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    align-items: center;
                    height: 100%;
                    margin: 0;
                    padding: 10px;
                    background-color: #F3F3F3;
                    font-family:"Encode Sans", sans-serif;
                    }
                .ContenedorTicket {
                    border: 2px solid rgba(0, 0, 0, 0.473);
                    box-shadow: 0px 10px 10px 0px rgba(0,0,0,0.4);
                    border-radius: 10px;
                    background-color: #ffffffa8;
                    padding: 10px;
                    width: 50%;
                    font-family:"Encode Sans", sans-serif;
                }
                
               
                .ContenedorTicket p {
                    margin: auto;
                    padding: 10px;
                    font-family:"Encode Sans", sans-serif;
                }
                .Titulo {
                    background-image: repeating-linear-gradient(45deg, rgba(0,0,0,0.06),transparent,rgba(0,0,0,0.08),rgba(0,0,0,0.1),rgba(0,0,0,0.1),rgba(0,0,0,0.06),rgba(0,0,0,0.04),transparent,rgba(0,0,0,0.07),rgba(0,0,0,0.06),rgba(0,0,0,0.1) 3px),linear-gradient(90deg, rgb(39,157,46),rgb(38,186,195));    -webkit-font-smoothing: antialiased; 
                    color: white;
                    height: 30px;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0px 0px;
                    font-family:"Encode Sans", sans-serif;
                }
             
                .footer {
                    display: flex;
                    justify-content: center;                    
                    background-image: repeating-linear-gradient(45deg, rgba(0,0,0,0.06),transparent,rgba(0,0,0,0.08),rgba(0,0,0,0.1),rgba(0,0,0,0.1),rgba(0,0,0,0.06),rgba(0,0,0,0.04),transparent,rgba(0,0,0,0.07),rgba(0,0,0,0.06),rgba(0,0,0,0.1) 3px),linear-gradient(90deg, rgb(39,157,46),rgb(38,186,195));    -webkit-font-smoothing: antialiased; 
                    color: white;
                    height: 30px;
                    margin: 0;
                    padding: 20px;
                    text-align: center;
                    border-radius: 0px 0px 5px 5px;
                    font-family:"Encode Sans", sans-serif;
                }
                .image{
                    display: flex;
                    justify-content: center;
                    align-items:center;
                    margin: 20px auto;
                    align-items: center;
                    width: 80%;
                }
                .image img{
                    margin: auto;
                    
                }
                a {
                    text-decoration: none;
                }
                </style>
            </head>
            <body>
                <div class="ContenedorTicket">
                    <div class="image">
                        <a href="requerimientos.prome.ar">
                            <img src="https://requerimientos.prome.ar/assets/Recurso%206@0.75x.png" width="80%">               
                        </a>
                    </div> 
                    """
                    + str(mapearCuerpoDeCorreo(data, id)) +
                    """<p class="footer"><b>Por favor, No responda este email</b></p>
                    
                </div>
            </body>
        </html>
        """)
    
    return body


def enviarCorreo(destinatarios: list, asunto: str, _mensaje: str, bcc_destinatarios: list = []):
    cuerpo_mensaje = _mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = EMAIL_REMITENTE
    mensaje['Subject'] = asunto
    mensaje.attach(MIMEText(cuerpo_mensaje, 'html', 'utf-8'))

    # Establecer destinatarios en el encabezado To
    mensaje['To'] = ",".join(destinatarios)

    # Agregar destinatarios en el encabezado Bcc
    if bcc_destinatarios:
        mensaje['Bcc'] = ",".join(bcc_destinatarios)

    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        # print('Conexion exitosa al servidor de GMAIL')
    except Exception as e:
        print(f'Error al conectarse al servidor de Gmail: {e}')

    try:
        # Se loguea
        server.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
        # Enviar mensaje
        texto = mensaje.as_string()
        server.sendmail(EMAIL_REMITENTE, destinatarios + bcc_destinatarios, texto)
        server.quit()
        print("Email enviado exitosamente")
        
    except Exception as e:
        print('Error en el envío de correo', e)

def enviarCorreoDeError(_asunto: str, error:str):
    
    print(_asunto)
    print(error)
    
    correosDeError: list =  ["mmillan@provinciamicrocreditos.com"]
    mensaje: str =  f"Error al crear el requerimiento ->  {str(error)}"
    asunto: str = f"Error en GDR: {str(_asunto)}"
    print(_asunto)
    print(error)
    print(type(_asunto))
    print(type(error))
    enviarCorreo(correosDeError, asunto, mensaje, ['mbarreto@provinciamicrocreditos.com','mjmillan@fi.uba.ar'])
    
    
if __name__ == "__main__":
    
    destinatarios: list = ["mmillan@provinciamicrocreditos.com"]
    enviarCorreo("mmillan@provinciamicrocreditos.com","prueba", "GDR prueba")
    print(str(",".join(destinatarios)))
    