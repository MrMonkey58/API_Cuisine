# __init__.py

"""
Projet option SIN I2 2023/2024 - UniLasalle Amiens

Créateurs:
    - MARTIN Tom
    - TRIVES VAN BOXSTAEL Arthur

Cf: main.py
"""

# Imports
import flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DB_NAME = "database.db"

# Création de l'application
def create_app():
    # Création du fichier de la base de données
    # Création application flask
    app = flask.Flask(__name__)
    app.config["SECRET_KEY"] = "pzuhdtrht515038eqefdqdf58jknqdp^lkafijrzpojzrpmae31521235aefaef3521aefyjr"

    # Chemin d'accès à la base de données
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'

    # Lie la base de données avec l'application
    db.init_app(app)

    # On inscrit un blueprint (du fichier routes.py) à l'application
    from .routes import views
    app.register_blueprint(views, url_prefix="/")

    # Création de la base de données
    create_database(app)
    return app

# Création de la base de données
def create_database(app):
    with app.app_context():
        # Si la base de données n'existe pas, on la créée
        if not path.exists('../instance/'+ DB_NAME):
            db.create_all()
            print("Base de données créée")
