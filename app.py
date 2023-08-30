import os
from flask import Flask, jsonify, request
from flask_cors import CORS

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

# USER: str = settings.DBUSER
# PASS: str = settings.DBPASS
# SERVER: str = settings.DBSERVER
# NAME: str = settings.DBNAME

# # getUserForProject_bp = Blueprint("getUserForProject_bp", __name__)
# conn_str = str(f"mssql+pyodbc://{USER}:{PASS}@{SERVER}/{NAME}?driver=ODBC+Driver+17+for+SQL+Server")

app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = conn_str
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# ma = Marshmallow(app)

    

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

app.static_folder = 'static'
app.template_folder='templates'


if __name__ == '__main__':
    
    try:    
        os.mkdir('docs/tmpFilesReceived/')
        app.run()
    except Exception as e:
        print(f'Ocurrio un error en la ejecución: {e}') 
