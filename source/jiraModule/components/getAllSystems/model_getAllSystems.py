from source.jiraModule.utils.conexion.db import Base
from sqlalchemy import Column, Integer, String, Text


class AprobadoPor(Base):
    __tablename__ = 'GDR_Systems'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True)
    description = Column(Text, unique=True)
    active = Column(String(80), unique=True, nullable=False)
    
    
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

