import random
import string

def generateRandomToken(length=120):
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(length))
    return token


