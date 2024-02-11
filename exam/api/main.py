from flask import Flask, render_template, request, make_response, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import mysql.connector
import bcrypt
import jwt
import env
from datetime import datetime

# Connexion à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    user="adm",
    password="r00t",
    database="projectdb"
)

# Clé secrète
jwt_secret_key = "MAsuperclé"

app = Flask(__name__)
app.secret_key = "r00t"

# Déclaration de la classe LoginForm
class LoginForm(FlaskForm):
    mail = StringField('Mail',render_kw={"placeholder": "Email"}, validators=[DataRequired()])
    password = PasswordField('Password',render_kw={"placeholder": "Mot de passe"}, validators=[DataRequired()])
    submit = SubmitField('Connexion')

@app.route("/", methods=['GET','POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        mail = form.mail.data
        password = bcrypt.hashpw(form.password.data.encode('utf-8'), env.salt)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT password, is_teacher FROM exam_user WHERE mail = %s", (mail,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            stored_hashed_password = user_data['password']
            if str(password) == stored_hashed_password:
                # Si le mot de passe est vérifié --> Génération du token JWT
                jwt_token = generate_jwt(mail)
                # Vérification si l'utilisateur est un enseignant ou un étudiant
                if user_data['is_teacher'] == False:
                    if session_validity("2") == True:
                        # Préparation de la réponse avec une redirection
                        response = make_response(render_template('form.html'))
                        # Mise à jour des cookies dans la réponse
                        response.set_cookie('jwt',jwt_token)
                    else:
                       return make_response(render_template('form_close.html'))
                else:
                    response = make_response(redirect("http://127.0.0.1:8000/teacher"))
                    # Mise à jour des cookies dans la réponse
                    response.set_cookie('jwt',jwt_token)
                    return response
                return response
            else:
                # Utilisateur existant mais mot de passe erroné
                return "La combinaison mail / mot de passe est erronée"
        else:
            # Utilisateur inexistant
            return "La combinaison mail / mot de passe est erronée"
    #Si la page n'a pas été appelée en POST et/ou si le formulaire n'est pas valide
    return render_template('login.html', form=form)

# Fonction de génération de token JWT
def generate_jwt(mail):
    payload = {'mail': mail}
    token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')
    return token


# Fonction de récupération de la session à partir de son Id
def get_session (id):
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT status, start_time, end_time FROM exam_session WHERE id = %s", (id,))
    session = cursor.fetchone()
    cursor.close()
    return session

# Fonction de vérification de la validité de la session
def session_validity(id):
    current_session = get_session(id)
    session_status  = current_session["status"]
    session_future = datetime.utcnow() < current_session["start_time"]
    session_over   = datetime.utcnow() > current_session["end_time"]

    if session_status == True:
        if session_future == False:
            if session_over == False:
                return True
            else:
                print("ok")
                return False
        else:
            print("ok2")
            return False
    else:
        return False

@app.route("/api/<mavalue>", methods=['POST'])
# Fonction de récupération du token JWT, décodage et récupération des informations
def api():
    data = request.json
    token = request.cookies.get('jwt')
    decoded = jwt.decode(token, jwt_secret_key, algorithms=['HS256'])
    mail = decoded.get('mail')

    # Vérifier si l'utilisateur a déjà des données en base
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM exam_answer WHERE mail = %s", (mail,))
    existing_data = cursor.fetchone()
    first_login = datetime.utcnow()

    if existing_data:
        # Si des données existent, mettre à jour les valeurs
        sql = "UPDATE exam_answer SET progression = %s, difficulty = %s, percent = %s WHERE mail = %s"
        values = (data['progression'], data['difficulty'], data['percent'], mail)
    else:
        # Si aucune donnée n'existe, insérer les nouvelles données
        sql = "INSERT INTO exam_answer (mail, progression, difficulty, percent, first_login) VALUES (%s, %s, %s, %s, %s)"
        values = (data['progression'], data['difficulty'], data['percent'], first_login, mail)

    cursor.execute(sql, values)
    mydb.commit()
    cursor.close()
    return "ok"


@app.route("/form")
def form():
    return render_template('form.html')

if __name__ == "__main__":
    app.run(debug=True)