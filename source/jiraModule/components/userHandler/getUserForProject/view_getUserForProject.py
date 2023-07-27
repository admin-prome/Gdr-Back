import json
from flask import Blueprint, jsonify
from source.jiraModule.components.userHandler.getUserForProject.controller_getUserForProject import getUsersByProject


getUserForProject_bp = Blueprint("getUserForProject_bp", __name__)

@getUserForProject_bp.route('/users/<project_key>', methods=['GET'])

def get_users(project_key):
    users = getUsersByProject(project_key)
    return jsonify(users)
