from datetime import datetime
import json

from source.modules.getRandomToken import generateRandomToken


class SessionModel:
    
    def __init__(self, userSession):
        self.userEmail: str = userSession['email'].title() 
        self.userName: str = userSession['name'].title()
        self.userIdJIRA: str = ''
        self.userSessionToken: str = self.setUserSessionToken()
        self.timestamp: str = self.get_timestamp()
        self.userDetails: dict = {}
        self.session: dict = {
            'timestamp': self.timestamp,
            'userSession': self.userSessionToken,
            'name': self.userName,
            'idJIRA': self.userIdJIRA,
            'email': self.userEmail,
            'details': self.userDetails
        }
    
    def get_timestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def setUserEmail(self, email: str) -> None:
        self.userEmail = email
        
    def getUserEmail(self)-> str:
        return self.userEmail    
    
    def setUserIdJIRA(self, id: str) -> None:
        self.session['idJIRA'] = id
        self.userIdJIRA = id
        
    def getUserIdJIRA(self) -> str:
        return self.userIdJIRA
    
    def setUserSessionToken(self) -> None:
       return generateRandomToken()
    
    def __str__(self):
        return f"Session for {self.userName} (ID: {self.userIdJIRA}, Email: {self.userEmail})"

    def __repr__(self):
        return f"SessionModel({self.userEmail}, {self.userName}, {self.userIdJIRA})"
    
    def getSession(self):
        return self.session
        
    def toJson(self):
        return json.dumps(self.session, indent=4)
    
    
    