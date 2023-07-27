import json
from flask import Blueprint, jsonify
from source.jiraModule.components.userHandler.getProjectsForUser.controller_getProjectsForUser import getProjectsForUser

getProjectForUser_bp = Blueprint("getProjectsForUser_bp", __name__)

@getProjectsForUser.route('/users/getprojectsforusers', methods=['GET'])
def getAllUsers() -> json:   
    
    response = getProjectsForUser()
    print(response)
    input('Aguarde view')
    return response