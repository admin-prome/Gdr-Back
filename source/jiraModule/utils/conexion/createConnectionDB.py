   
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import pyodbc

# Crear la clase base para declarar la estructura de la tabla
Base = declarative_base()

class Numerador(Base):
    __tablename__ = 'GDR_Contador'

    id = Column(Integer, primary_key=True)
    categoria = Column(String(80), unique=True, nullable=False)
    subcategoria = Column(String(80), unique=True, nullable=True)
    valor = Column(Integer, unique=True, nullable=False)

    def __init__(self, id, categoria, subcategoria, valor):
        self.id = id
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.valor = valor

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return f"<Numerador(id={self.id}, categoria={self.categoria}, subcategoria={self.subcategoria}, valor={self.valor})>"

def create_connection():
    # Cadena de conexión
    
    conn_str = 'mssql+pyodbc://mmillan:Promesa2024@172.17.12.216/PNET?driver=ODBC+Driver+17+for+SQL+Server'

    # Crear el motor de base de datos
    engine = create_engine(conn_str)

    # Crear la fábrica de sesiones
    Session = sessionmaker(bind=engine)

    # Retornar una sesión creada con la conexión establecida
    return Session()


if __name__ == '__main__':
    # Obtener la sesión
    session = create_connection()

    try:
        # Realizar operaciones en la base de datos utilizando la sesión
        result = session.query(Numerador).all()

        # Imprimir los resultados
        for row in result:
            print(row)

    except Exception as e:
        print(f"Ocurrió un error en la consulta: {e}")

    finally:
        # Cerrar la sesión
        session.close()
