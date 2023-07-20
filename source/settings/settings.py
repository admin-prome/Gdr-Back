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
    DBUSER_TST: str
    DBPASS_TST: str
    DBIP_TST: str
    DBIPPRIVATE_TST: str
    DBNAME_TST: str
    
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
    DBUSER_TST= os.getenv('DBUSER-TST'),
    DBPASS_TST= os.getenv('DBPASS-TST'),
    DBIP_TST=   os.getenv('DBIP-TST'),
    DBIPPRIVATE_TST=  os.getenv('DBIPPRIVATE-TST'),
    DBNAME_TST= os.getenv('DBNAME-TST')
    
    
    
    )


