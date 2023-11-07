import requests
from source.settings.settings import settings
from source.modules.getDetailsUser import model_getDetailsUser

URL: str = settings.URL_SERVICIOS_TECNO
KEY: str = settings.KEY_USER_DETAILS

def getUserDetails(email: str) -> dict:
    # Configurar el encabezado con el token de autorización
    headers = {
        "Authorization": KEY,
        "Content-Type": "application/json"
    }
    
    url = f'{URL}UserDetails/GetByEmail'

    try:
        print('Comienzo de getDetailsUser')
        # Realizar la solicitud GET al endpoint
        response = requests.get(url, params={"Email": email}, headers=headers)
        response.raise_for_status()  # Genera una excepción si el código de estado no es 2xx
       
        # Parsear la respuesta JSON a un diccionario
        response_data = response.json()

        # Crear una instancia de UserDetails a partir del JSON
        user_details = model_getDetailsUser.UserDetails.from_json(response_data['result'])
   
        return user_details.__dict__
    
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
    
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

    return {}  # Devolver un diccionario vacío en caso de error
