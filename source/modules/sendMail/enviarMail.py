from email.mime.text import MIMEText
import os
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart

def enviarMail(remitente:str, asunto: str, tokenPath: str):
    # Cargar el token de acceso obtenido de OAuth 2.0
    #token_path = 'ruta/al/token.json'
    creds = Credentials.from_authorized_user_file(token_path)

    # Crear el servicio de la API de Gmail
    service = build('gmail', 'v1', credentials=creds)

    # Crear el cuerpo del mensaje en formato MIME
    message = MIMEMultipart()
    message['to'] = 'mmillan@provinciamicrocreditos.com'
    message['from'] = remitente
    message['subject'] = f'{asunto}'

    # Agregar el contenido del correo electrónico
    body = 'Este es el cuerpo del correo electrónico.'
    message.attach(MIMEText(body, 'plain'))

    # Opcional: Adjuntar un archivo al correo electrónico
    # with open('archivo_adjunto.txt', 'rb') as attachment:
    #     att = MIMEText(attachment.read())
    #     att.add_header('Content-Disposition', 'attachment', filename='archivo_adjunto.txt')
    #     message.attach(att)

    # Codificar el mensaje en base64
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    # Enviar el correo electrónico utilizando la API de Gmail
    service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
    print('Correo electrónico enviado correctamente.')

if __name__ == '__main__':
    
    token_path = 'source/modules/token.json'
    enviarMail('mmillan@provinciamicrocreditos.com','prueba',token_path)
    