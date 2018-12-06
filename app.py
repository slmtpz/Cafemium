from flask import Flask, render_template, redirect, request, flash
import json
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from services import user_services
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY
from utils import decorators

app = Flask(__name__)
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)


def is_password_correct(hashed_password, given_password):
    return check_password_hash(hashed_password, given_password)


def get_hashed_password(given_password):
    return generate_password_hash(given_password)


@login_manager.user_loader
def load_user(user_email):
    user_instance = user_services.User(user_email)
    if user_instance.email_invalid:
        return None
    else:
        return user_instance


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        user_instance = load_user(email)
        if user_instance is None:
            flash('E-mail yanlış.')
            return redirect('login')
        elif is_password_correct(user_instance.password, password):
            login_user(user_instance)
            return redirect('cafe')
        else:
            flash('Şifre yanlış.')
            return redirect('login')

    else:
        return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')


@app.route('/')
def redirect_cafe():
    return redirect('cafe')


@app.route('/cafe')
@login_required
def serve_cafe_page():
    return render_template('cafe.html')


@app.route('/summary')
@login_required
@decorators.limit_to_role('client')
def serve_summary_page():
    return render_template('summary.html')


@app.route('/analysis')
@login_required
@decorators.limit_to_role('client')
def serve_analysis_page():
    return render_template('analysis.html')


@app.route('/authorities')
@login_required
def serve_authorities_page():
    return render_template('authorities.html')


@app.route('/user')
@login_required
def serve_user_page():
    return render_template('user.html')


@app.route('/signupClient', methods=['POST'])
@login_required
@decorators.limit_to_role('admin')
def register_new_client():
    firm_name = request.form['firm_name']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    if user_services.check_email(email):
        flash('Kayıt başarılı.')
        user_services.add_user('client', firm_name, name, email, phone, get_hashed_password(password))
    else:
        flash('Kayıt başarısız. Bu email adresi zaten kullanılıyor.')
    return redirect('user')


@app.route('/signupUser', methods=['POST'])
@login_required
@decorators.limit_to_role('client')
def register_new_user():
    firm_name = current_user.firm_name
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    if user_services.check_email(email):
        flash('Kayıt başarılı.')
        user_services.add_user('user', firm_name, name, email, phone, get_hashed_password(password))
    else:
        flash('Kayıt başarısız. Bu email adresi zaten kullanılıyor.')
    return redirect('user')


@app.route('/getSlots')
@login_required
def serve_slots():
    from random import randint
    slots = [{
        'name': 'Masa ' + str(randint(1, 10)),
        'bill': randint(2, 120),
        'time': randint(0, 120),
        'playerCount': randint(1, 4),
        'extraCount': randint(0, 5)
    } for _ in range(randint(7, 10))]

    return render_template('slots.html', slots=slots)


@app.route('/getSlotDetails/<slotName>')
@login_required
def get_javascript_data(slotName):
    return json.dumps({'name': slotName, 'details': 'this is from backend'})


if __name__ == '__main__':
    app.run()
