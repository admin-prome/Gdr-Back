import json
from flask import Blueprint, jsonify
from source.jiraModule.components.getLatestIssuesForProject import controller_getLatestIssuesForProject


getLatestIssuesForProject_bp = Blueprint("getLatestIssuesForProject", __name__)

@getLatestIssuesForProject_bp.route('/getlatestissuesforproject/<key_project>', methods=['GET'])

def GetProjects(key_project) -> json:   
    
    response = controller_getLatestIssuesForProject.getLatestIssuesForProject(key_project)
    
    return response

