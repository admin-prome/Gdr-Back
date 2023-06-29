from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#mailer@provinciamicrocreditos.com
CLIENTE = 'source/modules/token.json'
API_NAME = "gmail"
API_VERSION = "v1"
SCOPES = ["https://mail.google.com/"]

service = Create_Service(CLIENTE, API_NAME, API_VERSION, SCOPES)
mimeMessage = MIMEMultipart()
mimeMessage["subject"] = "este es el titulo"
emailMsg = "mensaje del mail"
mimeMessage["to"] = "mmillan@provinciamicrocreditos.com"

mimeMessage.attach(MIMEText(emailMsg, "plain"))

raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message = service.users().messages().send(userId = "me", body = {"raw": raw_string}).execute()
print(message)