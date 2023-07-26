# from utils.conexion.db import Base
from source.jiraModule.utils.conexion.db import Base
from sqlalchemy import Column, Integer, String


class GDR(Base):
    __tablename__ = 'GDR'
    
    Id = Column(Integer, primary_key=True)
    nombre = Column(String(80), unique=True, nullable=False)
    descripcion = Column(String(120), unique=True, nullable=False)

    def __init__(self, Id, nombre, descripcion):
        self.Id = Id
        self.nombre = nombre
        self.descripcion = descripcion
            
    def __str__(self):
        return self.nombre
    
    def __repr__(self):
        return '<nombres %r>' % self.nombre
    

class AprobadoPor(Base):
    __tablename__ = 'GDR_AprobadoPor'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(80), unique=True, nullable=False)
    idJIRA = Column(String(255), unique=True, nullable=False)
    nombre = Column(String(80), unique=True, nullable=False)
    area = Column(String(80), unique=True, nullable=False)
    
    def __init__(self, id, email, idJIRA, nombre, area):        
        self.id = id
        self.email = email
        self.idJIRA = idJIRA
        self.nombre = nombre
        self.area = area

    def __str__(self):
        # Método para representación de cadena amigable para el usuario
        return f"AprobadoPor: {self.nombre} (ID: {self.id}, Email: {self.email}, ID JIRA: {self.idJIRA}, Area: {self.area})"

    def __repr__(self):
        # Método para representación de cadena más detallada, útil para depuración
        return f"AprobadoPor(id={self.id}, email='{self.email}', idJIRA='{self.idJIRA}', nombre='{self.nombre}', area='{self.area}')"
