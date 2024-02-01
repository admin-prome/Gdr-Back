from sqlalchemy import create_engine
from source.settings.settings import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


USER: str = settings.DBUSER
PASS: str = settings.DBPASS
SERVER: str = settings.DBSERVER
NAME: str = settings.DBNAME

# Crear la cadena de conexión
conn_str = f"mssql+pyodbc://{USER}:{PASS}@{SERVER}/{NAME}?driver=ODBC+Driver+17+for+SQL+Server"

# Crear el motor de SQLAlchemy
engine = create_engine(conn_str)

# Crear una fábrica de sesiones
Session = sessionmaker(bind=engine)

# Inicializar la sesión
session = Session()

# Declarar la base de datos SQLAlchemy
Base = declarative_base()

# Imprimir un mensaje de inicio de conexión
print(f'Inicio de Conexión con BD: {NAME}')


