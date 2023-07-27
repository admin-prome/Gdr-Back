import json

data = {
  'key': 'GDD',
  'summary': 'prueba',
  'description': 'a',
  'type': 'Epic',
  'approvers': '6228d69b4160640069ca557b',
  'impact': 'a',
  'attached': 'a',
  'managment': 'a',
  'priority': 'Alta',
  'userCredential': {
    "iss": "https://accounts.google.com",
    "nbf": 1685454974,
    "aud": "688079392079-bpsjl4kmg4vuqik4562slb4ni6o9netb.apps.googleusercontent.com",
    "sub": "115753620167202415367",
    "hd": "provinciamicrocreditos.com",
    "email": "mmillan@provinciamicrocreditos.com",
    "email_verified": True,
    "azp": "688079392079-bpsjl4kmg4vuqik4562slb4ni6o9netb.apps.googleusercontent.com",
    "name": "Maximiliano Juan Millan",
    "picture": "https://lh3.googleusercontent.com/a/AAcHTtds4yjEFHZDh1TI-tLBLkRBgWtQqY_Ag0MkUqxh=s96-c",
    "given_name": "Maximiliano Juan",
    "family_name": "Millan",
    "iat": 1685455274,
    "exp": 1685458874,
    "jti": "cee11d5bfdff6886ae55d42a7169c61a473b1e96"
  },
  'initiative': ''
}

json_data = json.dumps(data)
print(json_data)
