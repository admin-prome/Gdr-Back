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
    DBIP: str
    DBIPPRIVATE: str
    DBNAME: str
    DEVCLIENTID: str
    DEVCLIENSECRET: str
    EMAIL_REMITENTE: str
    EMAIL_PASSWORD: str
    
load_dotenv()

settings = Settings(
    DOMAIN= os.getenv('DOMAIN'),
    MAIL=   os.getenv('MAIL'),
    APIKEY= os.getenv('APIKEY'),
    ENVIROMENT= os.getenv('ENVIROMENT'),
    DBUSER= os.getenv('DBUSER'),
    DBPASS= os.getenv('DBPASS'),
    DBIP=   os.getenv('DBIP'),
    DBIPPRIVATE=  os.getenv('DBIPPRIVATE'),
    DBNAME= os.getenv('DBNAME'),
    DEVCLIENTID= os.getenv('DEVCLIENTID'),
    DEVCLIENSECRET= os.getenv('DEVCLIENSECRET'),
    EMAIL_REMITENTE= os.getenv('EMAIL_REMITENTE'),
    EMAIL_PASSWORD= os.getenv('EMAIL_PASSWORDT')
    )


