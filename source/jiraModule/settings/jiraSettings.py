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

env_path = os.path.join(os.path.dirname(__file__), 'jira.env')
load_dotenv(dotenv_path=env_path)

settings = Settings(
    DOMAIN=os.getenv('DOMAIN'),
    MAIL=os.getenv('MAIL'),
    APIKEY=os.getenv('APIKEY'),
    ENVIROMENT=os.getenv('ENVIROMENT'),
    DBUSER=os.getenv('DBUSER'),
    DBPASS=os.getenv('DBPASS'),
    DBSERVER=os.getenv('DBSERVER')
    )


