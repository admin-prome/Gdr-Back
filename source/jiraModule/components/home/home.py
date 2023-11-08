from flask import Blueprint, abort, render_template, session

home_bp = Blueprint("home_bp", __name__,template_folder='templates')
# , __name__, template_folder='app/templates'
def login_is_required(function):
    def wrapper(*args, **kwargs):
        print(session)
        if 'google_id' not in session:
            abort(401)  # Devuelve un error 401 si el usuario no ha iniciado sesión
        else:
            return function()
    return wrapper  # Asegúrate de devolver la función "wrapper"

    



@home_bp.route('/home', methods=['GET'])
@login_is_required
def ping():
    return render_template('index.html')
