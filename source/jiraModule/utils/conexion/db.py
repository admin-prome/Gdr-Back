from sqlalchemy import create_engine
from source.settings.settings import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pyodbc  

#print(pyodbc.drivers())
USER: str = settings.DBUSER
PASS: str = settings.DBPASS
SERVER: str = settings.DBSERVER
NAME: str = settings.DBNAME
# TST_USER: str = settings.DBUSER_TST
# TST_PASS: str = settings.DBPASS_TST
# TST_NAME: str = settings.DBNAME_TST
# TST_IP: str = settings.DBIP_TST


#conn_str = str(f"mssql+pyodbc://{TST_USER}:{TST_PASS}@{TST_IP}/{TST_NAME}?driver=ODBC+Driver+17+for+SQL+Server")
conn_str = str(f"mssql+pyodbc://{USER}:{PASS}@{SERVER}/{NAME}?driver=ODBC+Driver+17+for+SQL+Server")


engine = create_engine(conn_str)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()





print(f'Inicio de Conexión con BD: {NAME}')


# db = SQLAlchemy()

# app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql://{USER}:{PASS}@{IP}/pnet'



