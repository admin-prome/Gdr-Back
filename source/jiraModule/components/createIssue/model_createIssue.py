
from types import SimpleNamespace
from source.jiraModule.utils.conexion import db
from sqlalchemy import Column, Integer, String


class Issue:
    
    idTask: int = 0
    
    def __init__(self, data):
        # self.project = data['project']        
        self.key = data['key']
        self.summary = data['summary']
        self.description = data['description']
        self.type = data['type']
        self.issueType = data['issueType']
        self.subIssueType = data['subIssueType']
        self.approvers = SimpleNamespace(**data['approvers']) if 'approvers' in data else None
        self.impact = data['impact']
        self.attached = data['attached']
        self.managment = data['managment']
        self.priority = data['priority']
        self.initiative = data['initiative']
        self.normativeRequirement = data['normativeRequirement']
        self.finalDate = data['finalDate']
        self.normativeDate = data['normativeDate']
        self.userCredential = SimpleNamespace(**data['userCredential']) if 'approvers' in data else None 
        self.reporter = {"accountId": "","accountType": "atlassian"}
        
    # def __str__(self):
    #     return f"Summary: {self.summary}, Type: {self.type}, Priority: {self.priority}"

    # def __repr__(self):
    #     return f"MyObject({self.__dict__})"

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
            Titulo del requerimiento: [{self.issueType}-{self.subIssueType} XXX] {self.summary}           
            Prioridad definida por el usuario: {self.priority} 
            Aprobado por: {self.approvers.name} - {self.approvers.email}
            Gerencia: {self.approvers.management}             
            Enlace: {self.attached}
            Rol: {self.managment} 
            Funcionalidad: {self.description}
            Beneficio: {self.impact}
            Iniciativa: {self.initiative}
            Fecha de implementación: {self.finalDate} 
            Fecha normativa: {self.normativeDate}
            
            
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

    def setReporter(self, reporter: str) -> None:
        self.reporter['accountId'] = reporter
        
        
        
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
