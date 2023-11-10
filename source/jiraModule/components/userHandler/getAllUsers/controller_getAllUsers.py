# url = "https://your-domain.atlassian.net/rest/api/2/user/email"
import json
from source.jiraModule.utils.conexion.conexion import Conexion
from  source.modules.jsonTools.generarJSON import generate_and_save_json
from source.jiraModule.components.userHandler.getProjectsForUser.controller_getProjectsForUser import getProjectsForUser

def getTotalUsers():
    conexion = Conexion()
    response = conexion.get("/users/search")
   
    data = json.loads(response.text) 
    total = data[0]
    print(total)
    return total

def getUserMail(account_id):
   
    conexion = Conexion()
    
    url = f"/user?accountId={account_id}"
    
    try:
        response = conexion.get(path= url)
        response.raise_for_status()  # Comprobar si hubo un error en la respuesta del servidor
        
        data = response.json()
        print(data)
        email = data.get("emailAddress")
        print(email)
        return email
    except Exception as e:
        print('Ocurrió un error al obtener el email del usuario:', e)
        return None




def getUsersMails(accountId: str) -> json:
    conexion = Conexion()
    params = {
        'accountId': 'f6228d6e814cd2400690be43a'
    }
    
    try:
        response = conexion.get(f"user/email", params)
        print(f'Esto es el response: {response.text}')
        response.raise_for_status()  # Comprobar si hubo un error en la respuesta del servidor
        input('presione enter')
        return response
    except Exception as e:
        print('Ocurrió un error en la solicitud de email:', e)
        return None

def getAllUsers():
    conexion = Conexion()
    all_users = []

    start_at = 0
    max_results = 50
    total = getTotalUsers()
    contador: int = 0
    
    while True:
        params = {
            "startAt": start_at,
            "maxResults": max_results
        }
        response = conexion.get("users", params)
        
        print('##################################')
        print(total)
        print(contador)
        print(start_at)
        contador +=1
        print('##################################')
        data = json.loads(response.text)
        all_users.extend(data)
        total = int(len(data) + 100)
        
        start_at += max_results
        print('##################################')
        print('##################################')
        print(start_at)
        print('##################################')
        print('##################################')
        if len(all_users) >= total:
            print(f'len all user: {len(all_users)}')
            break

    user_list = []
    user_dict = {}
    contador: int = 0
    for user in all_users:        
        if user['active'] == True:
            contador+=1
            #userMail: str = getUserMail(user["accountId"])
            user_dict[contador] = {"displayName": user['displayName'], 
                                   "accountId": user["accountId"],
                                   #"userEmail": userMail,
                                   "projects" : getProjectsForUser()
                                   }
            #input('presione enter para continuar')
            
    user_json = json.dumps(user_dict, ensure_ascii=False)
    generate_and_save_json(user_json, 'allUsers.json')
            
    
    for user in all_users:
        
        #userMail: str = getUserMail(user["accountId"])
        input('presione enter para continuar')
        user_list.append({
            "displayName": user["displayName"],
            "accountId": user["accountId"]
            #"userEmail": userMail
        })
        
        
        
    #print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    generate_and_save_json(all_users, 'allUsers.json')
    return user_json

# def getAllUsers():
#     conexion = Conexion()
#     response = conexion.get("/users")
#     print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
#     generate_and_save_json(response,'allUsers.json')
#     input('Aguarde controller')
#     return response

    