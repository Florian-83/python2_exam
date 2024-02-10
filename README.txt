# python2_exam

# Création & activation de l'environnement virtuel Python :
python3 -m venv ./venv-project
source venv-project/bin/activate

# Installation des librairies :
pip install -r requirements.txt

# Initialisation Django :
django-admin startproject exam .

# Création d'une base de données :
mysql -u root -p
CREATE DATABASE projectdb;
GRANT ALL PRIVILEGES ON projectdb.* TO 'adm'@'localhost';
FLUSH PRIVILEGES;

# Modification du fichier "settings.py" :
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'projectdb',
        'USER': 'adm',
        'PASSWORD': 'r00t',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Créations des tables :
python manage.py makemigrations
python manage.py migrate

# Création du super user :
python manage.py createsuperuser

# Lancement du serveur :
python manage.py runserver

# Création des modèles de données :
-> Créer un nouveau fichier "models.py" dans la racine du projet
from django.db import models



