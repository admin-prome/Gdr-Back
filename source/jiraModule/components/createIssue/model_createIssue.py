
from types import SimpleNamespace
from source.jiraModule.utils.conexion import db
from sqlalchemy import Column, Integer, String
import json

from source.modules.getDetailsUser.model_getDetailsUser import UserDetails


class Issue:
    
    idTask: int = 0
    
    def __init__(self, data):
        # self.project = data['project']        
        self.key = self.get_data(data,'key')
        self.summary = self.get_data(data,'summary')
        self.description = self.get_data(data,'description')
        self.type = self.get_data(data, 'type')
        self.issuetype = self.get_data(data,'issuetype')
        self.subissuetype = self.get_data(data,'subissuetype')
        self.approvers = Approver(data['approvers'])
        self.impact = self.get_data(data, 'impact')
        self.attached = self.get_data(data, 'attached')
        self.managment = self.get_data(data, 'managment')
        self.priority = self.get_data(data, 'priority')
        #self.initiative = data['initiative']
        #self.normativeRequirement = data['normativeRequirement']
        self.finalDate = self.get_data(data, 'finalDate')
        self.normativeDate = self.get_data(data, 'normativeDate')
            
        self.userCredential = self.userCredential = UserCredential(data['userCredential'])
        self.isTecno = self.get_data(data, 'isTecno')

        self.reporter = self.setReporter(data['userCredential'])
    
    def get_data(self, data, key):
        try:
            return data[key]
        except KeyError:
            print(f'No se encontró {key}')
            return ''
        
    def setReporter(self, data) -> dict:
        try:
            if (data['idJIRA']):
                print('inicio de set reporter')   
                print(data['idJIRA'])           
                reporter = {"accountId": data['idJIRA'],"accountType": "atlassian"}
               
            else: 
                reporter = {"accountId": "6228d8734160640069ca5686","accountType": "atlassian"}
                print(reporter)
                
        except Exception as e:
            print(f'No se encontro el id de JIRA {e}')
            reporter = {"accountId": "6228d8734160640069ca5686","accountType": "atlassian"}
            print(reporter)
    
        return reporter
        
    def format_approvers(self):
        if self.approvers:
            return f"Aprobado por: {self.approvers.name} - {self.approvers.management}"
        else:
            return "No Approvers"

    
    def __str__(self):
        
        content: str = f'''
            Usuario informador: {self.reporter}
            Creado por: {self.userCredential.name}
            Email: {self.userCredential.email}
            Nombre del proyecto: {self.key} 
            Titulo del requerimiento: [{self.issuetype}-{self.subissuetype} XXX] {self.summary}           
            Prioridad definida por el usuario: {self.priority} 
            Aprobado por: {self.approvers.name} - {self.approvers.email}
            Gerencia: {self.approvers.management}             
            Enlace: {self.attached}
            Rol: {self.managment} 
            Funcionalidad: {self.description}
            Beneficio: {self.impact}
            
            Fecha de implementación: {self.finalDate} 
            Fecha normativa: {self.normativeDate}
            Proyecto: {self.key}
            
            
        '''

        return content


    def __repr__(self):
        attrs = vars(self)
        attrs_str = ', '.join([f"{key}={value!r}" for key, value in attrs.items()])
        repr : str = f"<{self.__class__.__name__}({attrs_str})>"
        return repr
    
    def setIdTask(self, id: int) -> None:
            self.idTask = id

    def getIdTask(self) -> int:
        return self.idTask
    
    def setKey(self, key: str) -> None:
        self.key = key

    # def setReporter(self, reporter: str) -> None:
    #     self.reporter['accountId'] = reporter


class Approver:
    def __init__(self, data):
        self.email = data['email']
        #self.id = data['id']
        self.management = data['management']
        try:
            self.name = data['name']
        except:
            self.name = data['label']
        self.value = data['value']

class UserCredential:
    def __init__(self, data):
        try:
           
            self.email = data['email']
            self.name = data['name']
            self.exp = data['exp']
            self.picture = self.setPicture(data)
            self.idJIRA = data['idJIRA']
            self.timestamp = data['timestamp']
            self.userSession = UserDetails(data['userSession'])
            
        except Exception as e: print(f'Ocurrio un error al mapear UserCredential: {e}')
        
    
    def setPicture(self, data):        
        try:
            self.picture = data['picture']
        except:
            self.picture = 'https://requerimientos.prome.ar/assets/logoColorP.png'

        
class IDRequerimientos(db.Base):
    __tablename__ = 'dbo.GDR_REQUERIMIENTOS'
    
    id_req = Column(Integer, primary_key=True)
    titulo = Column(String(80), unique=True, nullable=False)
    descripcion = Column(String(120), unique=True, nullable=False)

    def __init__(self, id_req, titulo, descripcion):
        self.id_req = id_req
        self.titulo = titulo
        self.descripcion = descripcion
            
    def __str__(self):
        return self.id_req
    
    def __repr__(self):
        return '<id_req %r>' % self.id_req    
    
    
class Numerador(db.Base):
    __tablename__ = 'GDR_Contador'
    
    id = Column(Integer, primary_key=True)
    categoria = Column(String(80), unique=True, nullable=False)
    subcategoria = Column(String(80), unique=True, nullable=True)
    valor = Column(Integer, unique=True, nullable=False)
    
    def __init__(self, id, categoria, subcategoria, valor):
        self.id = id
        self.categoria = categoria
        self.subcategoria = subcategoria
        self.valor = valor  # Agrega el igual y el valor de la variable
        
    def __str__(self):
        return str(self.id)  # Convierte el id a string
    
    def __repr__(self):
        return f"<Numerador(id={self.id}, categoria={self.categoria}, subcategoria={self.subcategoria}, valor={self.valor})>"
