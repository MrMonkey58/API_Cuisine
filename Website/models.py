# models.py

"""
Projet option SIN I2 2023/2024 - UniLasalle Amiens

Créateurs:
    - MARTIN Tom
    - TRIVES VAN BOXSTAEL Arthur

Cf: main.py
"""


# Imports
from . import db

# Table d'association pour les recettes favorites (update par rapport à User.recettes_preferees)
User_Recette = db.Table('recette_favorite',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('recette_id', db.Integer, db.ForeignKey('recette.id'))
                        )

User_Menu = db.Table('User_Menu',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'))
                     )


# Table pour un utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    pseudo = db.Column(db.String(100), unique=True, nullable=False)

    # Relation one-to-many avec Recette (les recettes que le l'user a créées)
    recettes = db.relationship("Recette", back_populates="auteur")

    # Relation many to many pour les recettes préférées
    recettes_preferees = db.relationship('Recette', secondary=User_Recette, backref="followers")

    # Relation many to many pour les menus d'un utilisateur
    menus = db.relationship('Menu', secondary=User_Menu, backref="menu_users")

    # backref ajoute une "fausse colonne" à l'enfant (qui est Recette ou Menu)


# Table pour un ingrédient
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)


# Cette table va contenir toutes les quantités utilisées pour chaque recette
class Quantite_Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantite = db.Column(db.String)  # ex : 200g, 1cc, 1cs, ...

    # Ces deux clés étrangères font le lien entre l'ingrédient utilisé ainsi que la recette
    recette_id = db.Column(db.Integer, db.ForeignKey('recette.id'))
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))

    # Plusieurs objets Quantite_Ingredient peuvent être associés à une seule recette (many-to-one)
    # Création d'une pseudo-colonne quantites dans la classe Recette
    recette = db.relationship('Recette', backref='quantites')

    # Problème de sérialisation en json donc création d'une fonction
    def to_dict(self):
        return {
            'quantite': self.quantite,
        }


# Table d'association pour les ingrédients des recettes (update par rapport à Recette.ingredients)
Recette_Ingredient = db.Table('recette_ingredient', db.Column('recette_id', db.Integer, db.ForeignKey('recette.id')),
                              db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id')),
                              )


# Table pour une recette
class Recette(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Constantes de la recette
    nom = db.Column(db.String(200))
    temps_prepa = db.Column(db.Integer)  # (en minutes)
    difficulte = db.Column(db.Integer)
    note = db.Column(db.Float)
    instructions = db.Column(db.String(9000))
    nombre_convives_de_base = db.Column(db.Integer)

    # Relations avec les autres tables
    ingredients = db.relationship('Ingredient', secondary=Recette_Ingredient, backref='recettes')
    # Création d'une pseudo-colonne 'recettes' dans la table Ingredient

    # Une recette peut être associée à plusieurs quantités (one to many)
    quantites_ingredients = db.relationship('Quantite_Ingredient', back_populates='recette')

    # Many to one avec User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), )  # Chaque recette possède un auteur
    auteur = db.relationship("User", back_populates="recettes")


# Table pour un menu
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), unique=True)
    entree_id = db.Column(db.Integer, db.ForeignKey('recette.id'))
    plat_id = db.Column(db.Integer, db.ForeignKey('recette.id'))
    dessert_id = db.Column(db.Integer, db.ForeignKey('recette.id'))
