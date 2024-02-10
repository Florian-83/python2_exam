from flask import Flask, render_template, request, jsonify, make_response, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import mysql.connector
import bcrypt
import jwt
import env

# Connexion à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    user="adm",
    password="r00t",
    database="projectdb"
)

# Clé secrete
jwt_secret_key = "MAsuperclé"

app = Flask(__name__)
app.secret_key = "r00t"

# Déclaration de la classe LoginForm
class LoginForm(FlaskForm):
    mail = StringField('Mail',render_kw={"placeholder": "Email"}, validators=[DataRequired()])
    password = PasswordField('Password',render_kw={"placeholder": "Mot de passe"}, validators=[DataRequired()])
    submit = SubmitField('Connexion')

# Déclaration de la classe SignupForm
# class SignupForm(FlaskForm):
#     last_name = StringField('Last Name',render_kw={"placeholder": "Nom"}, validators=[DataRequired()])
#     first_name = StringField('First Name',render_kw={"placeholder": "Prénom"}, validators=[DataRequired()])
#     mail = StringField('Mail',render_kw={"placeholder": "Email"}, validators=[DataRequired()])
#     password = PasswordField('Password',render_kw={"placeholder": "Mot de passe"}, validators=[DataRequired()])
#     submit = SubmitField('Sign Up')

# @app.route("/register", methods=['GET','POST'])
# def signup_page():
#     register = SignupForm()


@app.route("/", methods=['GET','POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        mail = form.mail.data
        password = bcrypt.hashpw(form.password.data.encode('utf-8'), env.salt)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT password FROM exam_user WHERE mail = %s", (mail,))
        user_data = cursor.fetchone()

        if user_data:
            stored_hashed_password = user_data['password']

            if str(password) == stored_hashed_password:
                #Si mot de passe vérifié, alors je génère mon JWT
                jwt_token = generate_jwt(mail)
                #Je prepare ma réponse avec une redirection
                response = make_response(redirect(url_for('form')))
                #Dans ma réponse je mettrais a jour les cookies
                response.set_cookie('jwt',jwt_token)
                return response
            else:
                # Utilisateur existant mais mot de passe erroné
                return "La combinaison mail / mot de passe est erronée"
        else:
            # Utilisateur inexistant
            return "La combinaison mail / mot de passe est erronée"

    #Si la page n'a pas été appelée en POST et/ou si le formulaire n'est pas valide
    return render_template('login.html', form=form)

def generate_jwt(mail):
    #Generation de token
    payload = {'mail': mail,}
    token = jwt.encode(payload, jwt_secret_key, algorithm='HS256')
    return token

@app.route("/form")
def form():
    return render_template('form.html')


if __name__ == "__main__":
    app.run(debug=True)