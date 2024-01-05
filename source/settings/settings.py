from dotenv import load_dotenv
import os
from dataclasses import dataclass

@dataclass
class Settings:
    DOMAIN: str 
    MAIL: str 
    APIKEY: str
    ENVIROMENT: str
    DBUSER: str
    DBPASS: str
    DBSERVER: str
    DBIPPRIVATE: str
    DBNAME: str
    DEVCLIENTID: str
    DEVCLIENSECRET: str
    EMAIL_REMITENTE: str
    EMAIL_PASSWORD: str    
    DB_USER_TST: str
    DB_PASS_TST: str
    DB_IP_TST: str
    DB_IP_PRIVATE_TST: str
    DB_NAME_TST: str
    KEY_USER_DETAILS: str
    URL_SERVICIOS_TECNO: str
    KEY_GDR_FRONT: str
    URL_BACK : str

    
load_dotenv()

settings = Settings(
    DOMAIN= os.getenv('DOMAIN'),
    MAIL=   os.getenv('MAIL'),
    APIKEY= os.getenv('APIKEY'),
    ENVIROMENT= os.getenv('ENVIROMENT'),
    DBUSER= os.getenv('DBUSER'),
    DBPASS= os.getenv('DBPASS'),
    DBSERVER=   os.getenv('DBSERVER'),
    DBIPPRIVATE=  os.getenv('DBIPPRIVATE'),
    DBNAME= os.getenv('DBNAME'),
    DEVCLIENTID= os.getenv('DEVCLIENTID'),
    DEVCLIENSECRET= os.getenv('DEVCLIENSECRET'),
    EMAIL_REMITENTE= os.getenv('EMAIL_REMITENTE'),
    EMAIL_PASSWORD= os.getenv('EMAIL_PASSWORDT'),
    DB_USER_TST= os.getenv('DB_USER_TST'),
    DB_PASS_TST= os.getenv('DB_PASS_TST'),
    DB_IP_TST=   os.getenv('DBIP-TST'),
    DB_IP_PRIVATE_TST=  os.getenv('DB_IP_PRIVATE_TST'),
    DB_NAME_TST= os.getenv('DB_NAME_TST'),
    KEY_USER_DETAILS = os.getenv('KEY_USER_DETAILS'),
    URL_SERVICIOS_TECNO= os.getenv('URL_SERVICIOS_TECNO'),
    KEY_GDR_FRONT= os.getenv('KEY_GDR_FRONT'),
    URL_BACK= os.getenv('URLBACK')
        
    )


