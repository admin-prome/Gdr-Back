import json, requests, re
from flask import jsonify, request
from source.settings.settings import settings

# from google.oauth2 import id_token
# from google.auth.transport import requests as google_requests


def getSessionJiraUser(data: json):
    
    token_respuesta = data['credential']
    print(data['credetential'])
    
    #domain = conexion.__getattribute__(domain)
    # Intercambio del token de respuesta de Google por un token de acceso de Jira
    #url = f'https://provinciamicrocreditos.atlassian.net/rest/auth/1/session/oauth'
    url = 'https://provinciamicrocreditos.atlassian.net/rest/auth/1/session'
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    payload = {
        'oauth_token': token_respuesta,
        'provider': 'google',
        #'oauth_callback': 'https://localhost:5000'
        #"atl_token":token_respuesta
        #"googleToken": token_respuesta
    }

    response = requests.post(url, headers=headers, json=payload)
   
    try:         
        print(f'token jira user: {response.text}')
    except: 
        print(f'Error: {response.text}')
    
    if response.status_code == 200:
        # Extracción del token de acceso de Jira de la respuesta
        token_acceso = response.json()['access_token']
        return 'Inicio de sesión exitoso en Jira. Token de acceso: ' + token_acceso
    else:
        return 'Error en el inicio de sesión en Jira: ' + response.text


def get_jira_token(data):
    # Replace 'YOUR_JIRA_URL' with your Jira server URL
    jira_url = 'https://provinciamicrocreditos.atlassian.net'
    
    
    
    
    try:
        google_credential = data['credential']
    
        print(data['credential'])
        # Verify the Google sign-in credential and get the user information         
        # Exchange the Google access token for a Jira token
        response = requests.post(
            f'{jira_url}/rest/auth/1/session',
            headers={'Authorization': f'Bearer {google_credential}'}
        )
        
        # Check if the authentication was successful
        if response.status_code == 200:
            jira_token = response.json()['session']['value']
            print('--------------------------------------------')
            print(jira_token)
            print('--------------------------------------------')
            return jira_token
        else:
            print(f'Jira authentication failed: {response.text}')
    
    except ValueError as e:
        print(f'Invalid Google credential: {e}')
        
        
        
        
    jira_url = 'YOUR_JIRA_URL'
    jira_client_id = 'YOUR_JIRA_CLIENT_ID'
    jira_client_secret = 'YOUR_JIRA_CLIENT_SECRET'
    jira_redirect_uri = 'https://provinciamicrocreditos.atlassian.net'

    # Step 1: Exchange Google credential token for access token and ID token
    google_token_endpoint = 'https://oauth2.googleapis.com/token'
    google_token_params = {
        'code': google_credential,
        'client_id': jira_client_id,
        'client_secret': jira_client_secret,
        'redirect_uri': jira_redirect_uri,
        'grant_type': 'authorization_code'
    }

    google_token_response = requests.post(google_token_endpoint, data=google_token_params)
    google_token_data = google_token_response.json()
    id_token = google_token_data['id_token']

    # Step 2: Use ID token to obtain Jira token
    jira_token_endpoint = f'{jira_url}/rest/auth/1/session'
    headers = {'Authorization': f'Bearer {id_token}'}

    jira_token_response = requests.post(jira_token_endpoint, headers=headers)
    jira_token_data = jira_token_response.json()
    jira_token = jira_token_data['session']['value']

    return jira_token


class LoginJiraService:
    def __init__(self):
        self.api_url = 'https://auth.atlassian.com/authorize'
        # audience=api.atlassian.com
        # client_id=Zg1kfnn2umPy8NDHIkuF1pSbWwSUqSaL
        # scope=manage%3Ajira-configuration%20read%3Ajira-user%20manage%3Ajira-webhook%20write%3Ajira-work%20manage%3Ajira-project%20read%3Ajira-work%20manage%3Ajira-data-provider
        # redirect_uri=https%3A%2F%2Flocalhost%3A4200%2Fhome
        # state=${YOUR_USER_BOUND_VALUE}
        # response_type=code
        # prompt=consent

    def get_token(self, google_token):
        headers = {'Content-Type': 'application/json'}
        data = {
            'audience': 'api.atlassian.com',
            'client_id': settings.DEVCLIENTID,  # You need to define environment.clientId
            'scope': 'manage%3Ajira-configuration%20read%3Ajira-user%20manage%3Ajira-webhook%20write%3Ajira-work%20manage%3Ajira-project%20read%3Ajira-work%20manage%3Ajira-data-provider',
            'redirect_uri':'https://localhost:4200/home',
            'state': str(google_token),           
            'response_type': 'code',
            'prompt': 'consent'
            #'grant_type': 'authorization_code',
            #'client_secret': settings.DEVCLIENSECRET,  # You need to define environment.clientSecret
            #'code': google_token,  
        }
       
        try:
            response = requests.get(self.api_url, json=data, headers=headers)
            return(response)
            print('----------------------------')
            #response.raise_for_status()
            
            json_data = response.json()
            # Visualizar los datos obtenidos
            print('esto es el json data: {json_data}')
            
            return json_data
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None