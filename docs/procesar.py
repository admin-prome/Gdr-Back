import json

def leer_json_generar_txt(ruta_json, ruta_txt):
    with open(ruta_json) as f:
        data = json.load(f)

    with open(ruta_txt, 'w') as f:
        for key, value in data.items():
            display_name = value['displayName']
            account_id = value['accountId']
            f.write(f"{display_name}\t{account_id}\n")

# Uso de la función leer_json_generar_txt
ruta_json = 'docs/allUsers.json'
ruta_txt = 'docs/allUsers.txt'
leer_json_generar_txt(ruta_json, ruta_txt)
