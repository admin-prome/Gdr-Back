from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar_password():
    if request.method == 'POST':
        length = 12  # Longitud de la contraseña generada
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return render_template('index.html', password=password)

if __name__ == '__main__':
    app.run(debug=True)