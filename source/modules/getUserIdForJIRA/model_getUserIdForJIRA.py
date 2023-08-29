from sqlalchemy import Column, Integer, String
from source.jiraModule.utils.conexion.db import Base


class NominaUsersIds(Base):
    __tablename__ = 'tec_nomina'
    
    id = Column(Integer, primary_key=True)
    employeeNumber = Column(Integer, unique=True, nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    fullName = Column(String(80), unique=True, nullable=False)
    category = Column(String(80), unique=True, nullable=False)
    
    def __init__(self, id, email, idJIRA, fullName, category):        
        self.id = id
        self.email = email
        self.nombre = fullName
        self.categoria = category

    def __str__(self):
        # Método para representación de cadena amigable para el usuario
        return f"Nombre: {self.nombre} (ID: {self.id}, Email: {self.email}, Categoria: {self.area})"

    def __repr__(self):
        # Método para representación de cadena más detallada, útil para depuración
        return f"Nomina(id={self.id}, email='{self.email}', nombre='{self.nombre}', categoria='{self.categoria}')"
    

class JiraUsersId(Base):
    __tablename__ = 'tec_jiraIds'
    
    idUser = Column(Integer, primary_key=True)
    idJiraUser = Column(Integer, unique=True, nullable=False)
    
    def __init__(self, id, idJiraUser):        
        self.id = id
        self.jiraId = idJiraUser
 

    def __str__(self):
        # Método para representación de cadena amigable para el usuario
        return f"IdUSer: {self.id} (ID JIRA: {self.jiraId})"

    def __repr__(self):
        # Método para representación de cadena más detallada, útil para depuración
        return f"Id de JIRA (id={self.id}, idJIRA='{self.jiraId}')"