from flask import Flask, redirect, request, url_for, session
from flask_oauthlib.client import OAuth
# Configura los detalles de tu aplicación
CLIENT_ID = '688079392079-3v0vv38kbaqade3of9gaic9sj5k1ma14.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'http://localhost:4200/home'



app = Flask(__name__)

app.secret_key = 'tu-clave-secreta'

oauth = OAuth(app)

# Configura las credenciales de Google
google = oauth.remote_app(
    'google',
    consumer_key=CLIENT_ID,
    consumer_secret=CLIENT_SECRET,
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def index():
    if 'google_token' in session:
        user_info = google.get('userinfo')
        return 'Hola, {}!'.format(user_info.data['email'])
    return '¡Bienvenido! <a href="/login">Iniciar sesión con Google</a>'

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Acceso denegado: razón={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    return 'Hola, {}!'.format(user_info.data['email'])

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run()
