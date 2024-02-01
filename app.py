import os
import pathlib
import cachecontrol
from flask import Flask, abort, jsonify, redirect, request, session
from flask_cors import CORS
import google_auth_oauthlib
import requests
# from flask_cache import Cache

# from flask_sqlalchemy import SQLAlchemy                                                                                                                        
# from flask_marshmallow import Marshmallow
# from source.settings.settings import settings

from source.jiraModule.components.getLatestIssuesForProject.view_getLatestIssuesForProject import getLatestIssuesForProject_bp
from source.jiraModule.components.getAllProjects.view_getAllProjects import getAllProjects_bp
from source.jiraModule.components.test.test import test_bp
from source.jiraModule.components.createIssue.view_createIssue import createIssue_bp
from source.jiraModule.components.getIssues.getIssues import getIssues_bp
from source.jiraModule.components.getIssueForID.getIssueForID import getIssueForID_bp
from source.jiraModule.components.home.home import home_bp
from source.jiraModule.components.userHandler.getSessionJiraUser.view_getSessionJiraUser import loginJira_bp
from source.jiraModule.components.userHandler.getUserForEmail.view_getUserForEmail import getUserForEmail_bp
#from source.jiraModule.components.userHandler.getUserForProject.view_getUserForProject import getUserForProject_bp
from source.jiraModule.components.userHandler.getAllUsers.view_getAllUsers import getAllUsers_bp
from source.jiraModule.components.userHandler.getUserSession.view_getUserSession import getUserSession_bp

from source.jiraModule.components.userHandler.getProjectsForUser.view_getProjectsForUser import getProjectsForUser_bp
from source.jiraModule.components.getForm.view_getForm import getForm_bp
from source.settings.settings import settings

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport.requests import Request


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

KEY: str = settings.KEY_GDR_FRONT



app = Flask(__name__)
app.secret_key = "gdrback"






CORS(app, resources={r"/GetForm": {"origins": "http://localhost:4200"}})

cors = CORS(app, origins=["https://requerimientos.provinciamicrocreditos.com","https://gdrfront.azurewebsites.net" ],methods="POST")
CORS(app)
app.url_map.strict_slashes = False


app.register_blueprint(test_bp)
app.register_blueprint(createIssue_bp)
app.register_blueprint(getIssues_bp)
app.register_blueprint(getAllProjects_bp)
app.register_blueprint(getIssueForID_bp)
app.register_blueprint(home_bp)
app.register_blueprint(getLatestIssuesForProject_bp)
app.register_blueprint(getUserForEmail_bp)
#app.register_blueprint(getUserForProject_bp)
app.register_blueprint(getAllUsers_bp)
app.register_blueprint(loginJira_bp)
app.register_blueprint(getUserSession_bp)
app.register_blueprint(getProjectsForUser_bp)
app.register_blueprint(getForm_bp)

app.static_folder = 'static'
app.template_folder='templates'


@app.route('/')
def index():
    return "Por favor inicie sesión con su cuenta corporativa <a href='/login'><button>Login</button></a>"


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Esta función de middleware se ejecuta antes de cada solicitud
@app.before_request

def middleware_de_autorizacion():
    if request.method != 'OPTIONS':
        #if request.method == 'POST' and currentRoute == '/GetForm':
        # Verifica la clave y el origen de la solicitud en los encabezados
        authorization_key = request.headers.get('Authorization-Key')
        origin = request.headers.get('Origin')
        
        currentRoute = request.path
      
        if currentRoute == '/GetForm' or currentRoute =='/getissuesforuser':
            if authorization_key != KEY:
                # Si la clave o el origen son inválidos, retorna una respuesta de error
                return jsonify({'error': 'Acceso denegado'}), 403
    pass

if __name__ == '__main__':
    
    try:            
        app.run(debug=True)
        
    except Exception as e:
        print(f'Ocurrio un error en la ejecución: {e}') 
