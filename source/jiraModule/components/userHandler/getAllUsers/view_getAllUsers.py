import json
from flask import Blueprint, jsonify
from source.jiraModule.components.userHandler.getAllUsers import controller_getAllUsers

getAllUsers_bp = Blueprint("getAllUsers_bp", __name__)

@getAllUsers_bp.route('/users/getallusers', methods=['GET'])
def getAllUsers() -> json:   
    
    response = controller_getAllUsers.getAllUsers()
    input('Aguarde view')
    return response
    
    