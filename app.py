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

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
REDIRECT_URI = settings.REDIRECT_URI
#url: str = "https://gdr-back-tst.azurewebsites.net"
url = settings.URL_BACK
# # getUserForProject_bp = Blueprint("getUserForProject_bp", __name__)
# conn_str = str(f"mssql+pyodbc://{USER}:{PASS}@{SERVER}/{NAME}?driver=ODBC+Driver+17+for+SQL+Server")

app = Flask(__name__)
app.secret_key = "gdrback"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, './docs/token.json')


flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
                                     scopes=["https://www.googleapis.com/auth/userinfo.profile",
                                             "https://www.googleapis.com/auth/userinfo.email",
                                             "openid"], 
                                     redirect_uri=f"{url}/callback")

# app.config['SQLALCHEMY_DATABASE_URI'] = conn_str
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# ma = Marshmallow(app)


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

def login_is_required(function):
    def wrapper(*args, **kwargs):
        print('esta accediendo a una ruta protegida')
        if 'google_id' not in session:
            abort(401)  # Devuelve un error 401 si el usuario no ha iniciado sesión
        else:
            return function()
    return wrapper  # Asegúrate de devolver la función "wrapper"

@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)


@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)
    
    if not session['state'] == request.args['state']:
        abort(500)
    
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = Request(session=cached_session)  # Corregir la creación del objeto Request
    
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    
    print(id_info)
    
    if 'hd' in id_info and id_info['hd'] == 'provinciamicrocreditos.com':

        session['google_id'] = id_info.get('sub')
        session['name'] = id_info.get('name')
    
        return redirect('/home')
    return abort(401)

@app.route('/')
def index():
    return "Por favor inicie sesión con su cuenta corporativa <a href='/login'><button>Login</button></a>"


@app.route('/protected_area')
@login_is_required
def protected_area():
    return "Protected! <a href='/logout'><button>Logout</button></a>"

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
