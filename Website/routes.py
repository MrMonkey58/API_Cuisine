# routes.py

"""
Projet option SIN I2 2023/2024 - UniLasalle Amiens

Créateurs :
    - MARTIN Tom
    - TRIVES VAN BOXSTAEL Arthur

Cf. : main.py
"""


# Imports
from flask import Blueprint, jsonify, request
from . import db
from .models import User, Ingredient, Recette, Menu, Quantite_Ingredient
import re

# On crée un blueprint "views" dans lequel il y aura toutes nos routes(=url)
views = Blueprint("views", __name__)


# Route de test
@views.route("/", methods=["get"])
def home():
    return "Home"


# Route utilisateur avec fonctions ajout et suppression
@views.route("/user", methods=["POST", "DELETE"])
# Fonction ajout
def fct_user():
    # Ajout d'utilisateur
    if request.method == "POST":
        req_json = request.json
        nom = req_json['Nom']
        prenom = req_json['Prénom']
        pseudo = req_json['Pseudo']
        new_user = User(pseudo=pseudo, nom=nom, prenom=prenom)
        user = User.query.filter_by(pseudo=pseudo).first()
        # Utilisateur n'existe pas encore
        if not user:
            db.session.add(new_user)
            db.session.commit()
            return jsonify(pseudo=new_user.pseudo, nom=new_user.nom, prenom=new_user.prenom)
        # Utilisateur déjà existant
        else:
            return "[ERREUR] : Impossible de créer l'utilisateur car il existe déjà."
    # Supprime un utilisateur
    if request.method == "DELETE":
        req_json = request.json
        pseudo = req_json['Pseudo']
        user = User.query.filter_by(pseudo=pseudo).first()
        # Utilisateur présent
        if user:
            db.session.delete(user)
            db.session.commit()
            return "L'utilisateur a été supprimé."
        # Utilisateur non existant
        else:
            return "[ERREUR] : Cet utilisateur n'existe pas, impossible de le supprimer."
    else:
        # Retour méthodes prisent en charges
        return "[ERREUR] : Mauvaise méthode, POST ou DELETE acceptées."


@views.route("/get-recpipes-of-one-user", methods=['GET'])
def get_recipe_of_one_user():
    if request.method == "GET":
        req_json = request.json
        pseudo = req_json["Pseudo"]
        user = User.query.filter_by(pseudo=pseudo).first()
        if user:
            user_recettes = [i.nom for i in user.recettes]  # Récupération des noms des recettes uniquement
            return jsonify(liste_recette=user_recettes)

        else:
            return "[ERREUR] : L'utilisateur n'existe pas."

    else:
        return "[ERREUR] : Mauvaise méthode, GET accepté."


# Route ingrédient avec ajout, demande, suppression
@views.route("/ingredient", methods=["POST", "GET", "DELETE"])
def fct_ingredients():
    # Ajout ingrédient
    if request.method == "POST":
        req_json = request.json
        nom = req_json["Nom"]
        up = nom.upper()
        ingredient = Ingredient.query.filter_by(nom=up).first()
        new_ingredient = Ingredient(nom=up)
        if ingredient:
            return "[ERREUR] : L'ingrédient existe déjà."
        else:
            db.session.add(new_ingredient)
            db.session.commit()
            return "L'ingrédient a été ajouté."
    # Renvoi ingrédients existants
    if request.method == "GET":
        ingredients = Ingredient.query.all()
        ingredient_list = [{"id": ingredient.id, "nom": ingredient.nom} for ingredient in ingredients]
        return jsonify(ingredient_list)
    # Supprime un ingrédient
    if request.method == "DELETE":
        req_json = request.json
        nom = req_json["Nom"]
        up = nom.upper()
        ingredient = Ingredient.query.filter_by(nom=up).first()
        # Ingrédient existe
        if ingredient:
            db.session.delete(ingredient)
            db.session.commit()
            return "L'ingrédient a été supprimé."
        # Ingrédient n'existe pas
        else:
            return "[ERREUR] : L'ingrédient n'existe pas."
    else:
        # Retour méthodes prisent en charges
        return "[ERREUR] : Mauvaise méthode, POST / GET / DELETE acceptées."


def modifier_quantite_ingredients(quantites, nombreConvives, nombreInitialRecette):

    # Cette liste ne contient que les chiffres de chaque quantité (ne prend pas les lettres)
    numbers = []

    for temp_string in quantites:
        # Utilise une expression régulière pour trouver tous les chiffres dans la chaîne
        digits = re.findall(r'\d+', temp_string)

        # Convertit les chiffres en entiers et les ajoute à la liste des nombres
        numbers.extend([int(digit) for digit in digits])

    modified_quantites = []

    for i in range(len(quantites)):
        # On remplace les premiers caractères par ce que l'on vient de multiplier
        modified_quantite = quantites[i][len(str(numbers[i])):]  # Garde la partie non numérique
        modified_quantite = str(int(numbers[i]/nombreInitialRecette * nombreConvives)) + modified_quantite
        modified_quantites.append(modified_quantite)

    return modified_quantites


# Route recette
@views.route("/recipe", methods=["POST", "GET", "DELETE"])
def fct_recipe():
    # Ajout d'une recette
    if request.method == "POST":
        # ----- Gestion du JSON envoyé -----
        req_json = request.json

        # Attributs de Recette
        nom = req_json['Nom'].upper()
        temps_prepa = req_json['Temps_prépa']
        difficulte = req_json['Difficulté']
        note = req_json['Note']
        nombre_convives_de_base = req_json['Nombre_convives_de_base']

        # Récupération des ingrédients et des quantités associées
        ingredients_json = req_json['Ingrédients']

        instructions = req_json['Instructions']
        etapes = instructions.split("|")  # Formatage des instructions vers une liste (etapes)
        # Relation many-to-one pour l'auteur de la recette
        user_pseudo = req_json['Pseudo']
        user_id = User.query.filter_by(pseudo=user_pseudo).first()
        if user_id:
            user_id = user_id.id

            # ----- Gestion des ingredients -----
            # Création de deux listes pour y stocker nos valeurs finales après des tours de boucles
            ingredients_recette = []
            quantites_recette = []

            # Recette récupérée
            recipe = Recette.query.filter_by(nom=nom).first()

            # Recette non présente de base alors, on l'a créée
            if not recipe:
                # Création de la nouvelle recette
                new_recipe = Recette(temps_prepa=temps_prepa, nom=nom, note=note, difficulte=difficulte,
                                     instructions=instructions, user_id=user_id,
                                     nombre_convives_de_base=nombre_convives_de_base
                                     )

                # On regarde parcours le dictionnaire que l'on vient de rentrer
                for i in ingredients_json:
                    # Formatage en majuscule + récupération dans une variable :
                    nom_ingredient = (i["Nom"]).upper()
                    quantite = i['Quantité']

                    # Recherche de l'objet Ingredient correspondant au nom de l'ingrédient
                    ingredient_obj = Ingredient.query.filter_by(nom=nom_ingredient).first()

                    # Si cet objet n'est pas trouvé, alors ça veut dire que cet ingrédient n'a pas encore été créé
                    if not ingredient_obj:
                        return f"[ERREUR] : L'ingrédient {nom_ingredient} n'a pas été créé au préalable."

                    # Sinon, l'ingrédient est bien présent. On peut l'ajouter à la recette
                    else:
                        # Création d'une quantité d'ingrédient dans la table du même nom
                        quantite_ingredient = Quantite_Ingredient(quantite=quantite, ingredient_id=ingredient_obj.id)

                        # On ajoute dans nos listes finales les objets créés et récupérés
                        quantites_recette.append(quantite_ingredient)
                        ingredients_recette.append(ingredient_obj)

                # Sans cette ligne, les quantités n'étaient pas ajoutés dans la bdd
                for quantite_ingredient in quantites_recette:
                    db.session.add(quantite_ingredient)

                # On change les quantites de la recette pour les quantités que l'on a récupérées
                new_recipe.quantites = quantites_recette
                # Même chose avec les ingrédients
                new_recipe.ingredients = ingredients_recette

                # Update de la bdd
                db.session.add(new_recipe)
                db.session.commit()

                # --- Réponse ---

                # Création d'une liste de noms d'ingrédients à partir de la liste d'objets Ingredient pour la réponse de la requête
                ingredient_names = [ingredient.nom for ingredient in ingredients_recette]
                # Création d'une liste des quantités puisque l'objet Quantite_Ingredient n'est pas en JSON de base
                quantites_recette_json = [q.to_dict() for q in new_recipe.quantites]

                # Création d'un dictionnaire contenant pour chaque ingrédient sa quantité
                dict_ingredients = dict(zip(ingredient_names, quantites_recette_json))

                return jsonify(temps_prepa=new_recipe.temps_prepa, nom=new_recipe.nom, note=new_recipe.note,
                               difficulte=new_recipe.difficulte, ingredients=dict_ingredients,
                               etapes=etapes, user=user_id)

            # Sinon la recette existe déjà
            else:
                return "[ERREUR] : Impossible de créer la recette car elle existe déjà."

        else:
            return "[ERREUR] : L'utilisateur n'existe pas."

    if request.method == "GET":
        req_json = request.json
        nom = req_json['Nom'].upper()
        nombre_convives = int(req_json['Nombre_convives'])

        recipe = Recette.query.filter_by(nom=nom).first()
        ingredient_names = [ingredient.nom for ingredient in recipe.ingredients]
        quantites_recette = [q.quantite for q in recipe.quantites]

        quantites_recette = modifier_quantite_ingredients(quantites_recette, nombre_convives, recipe.nombre_convives_de_base)

        # Création d'un dictionnaire contenant pour chaque ingrédient sa quantité
        dict_ingredients = dict(zip(ingredient_names, quantites_recette))

        etapes = recipe.instructions.split("|")  # Formatage des instructions vers une liste (etapes)

        if recipe:
            return jsonify({
                "Id": recipe.id,
                "Nom": recipe.nom,
                "Ingrédients": dict_ingredients,
                "Etapes": etapes
            })
        else:
            return "[ERREUR] : La recette n'existe pas, vérifiez l'orthographe."

    if request.method == "DELETE":
        req_json = request.json
        nom = req_json['Nom'].upper()
        recipe = Recette.query.filter_by(nom=nom).first()
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return "La recette " + nom + " a été supprimé."
        else:
            return "[ERREUR] : La recette n'existe pas, vérifiez l'orthographe."
    else:
        # Retour méthodes prisent en charges
        return "[ERREUR] : Mauvaise méthode, POST, GET et DELETE sont acceptées."


def contraintes_satisfaites(contraintes, ingredients_recette):
    for ingredient in ingredients_recette:
        if ingredient not in contraintes:
            return False
    return True


# Lister toutes les recettes possibles (avec contraintes ou non)
@views.route("/get-all-recipe", methods=["POST", "GET", "DELETE"])
def get_all_recipes():
    if request.method == "GET":
        req_json = request.json
        contrainte_ingredients = [i.upper() for i in req_json["Ingrédients"]]  # On met les données en majuscules
        recettes_possibles = []  # Cette liste contient toutes les recettes possibles (sous forme d'objet "Recette")
        all_recettes = Recette.query.all()  # Récupère toutes les recettes de la bdd

        # Dans toutes nos recettes, on regarde le nom des ingrédients pour chacune d'entre-elles
        for recette in all_recettes:
            noms_ingredients_recette = [i.nom for i in recette.ingredients]

            # Si les ingrédients de contraintes sont les mêmes que les ingrédients de la recette alors, on peut la faire
            if contraintes_satisfaites(contrainte_ingredients, noms_ingredients_recette):
                recettes_possibles.append(recette)

        # On retourne les noms des recettes que l'on peut faire
        return jsonify(Recettes_possibles=[i.nom for i in recettes_possibles])


# Route recette aux favoris, ajout recette et retour recette selon utilisateur
@views.route("/favorite", methods=["POST", "GET", "DELETE"])
def fct_recipe_to_favorite():
    # Ajout recette aux favoris
    if request.method == "POST":
        req_json = request.json
        pseudo = req_json['Pseudo']
        nom = req_json['Nom'].upper()
        recipe = Recette.query.filter_by(nom=nom).first()
        user = User.query.filter_by(pseudo=pseudo).first()
        # Utilisateur et recette existent
        if user and recipe:
            if not (recipe in user.recettes_preferees):
                user.recettes_preferees.append(recipe)
                db.session.commit()
                return "Recette ajoutée dans les favoris !"
            else:
                return "[ERREUR] : Cette recette fait déjà partie de vos favoris."
        else:
            return "[ERREUR] : Les informations que vous avez fournies sont incorrectes/"

    # Renvoie recette dans ses favoris selon utilisateur
    if request.method == "GET":
        req_json = request.json
        pseudo = req_json['Pseudo']
        user = User.query.filter_by(pseudo=pseudo).first()
        liste_recettes_pref = [{"id": recette.id, "nom": recette.nom} for recette in user.recettes_preferees]
        if user:
            return jsonify(recettes_favorites=liste_recettes_pref)
        else:
            return "[ERREUR] : L'utilisateur ne possède pas de recettes en favoris."

    if request.method == "DELETE":
        req_json = request.json
        pseudo = req_json['Pseudo']
        nom = req_json['Nom'].upper()
        recipe = Recette.query.filter_by(nom=nom).first()
        user = User.query.filter_by(pseudo=pseudo).first()
        if recipe and user:
            user.recettes_preferees.remove(recipe)
            db.session.commit()
            return "La recette " + nom + " a été supprimé des favoris."
        else:
            return "[ERREUR] : Les informations fournies sont incorrectes."

    else:
        # Retour méthodes prisent en charges
        return "[ERREUR] : Mauvaise méthode, POST et GET acceptées."


@views.route("/menu", methods=["POST", "GET", "DELETE"])
def fct_menus():
    if request.method == "POST":
        # ---- Gestion du JSON ----
        req_json = request.json
        pseudo = req_json['Pseudo']
        nom_menu = req_json["Nom_menu"].upper()
        nom_entree = req_json["Nom_entrée"].upper()
        nom_plat = req_json["Nom_plat"].upper()
        nom_dessert = req_json["Nom_dessert"].upper()

        entree = Recette.query.filter_by(nom=nom_entree).first()
        plat = Recette.query.filter_by(nom=nom_plat).first()
        dessert = Recette.query.filter_by(nom=nom_dessert).first()
        user = User.query.filter_by(pseudo=pseudo).first()

        # On regarde si quelqu'un n'a pas déjà créé le même menu. Si c'est le cas, on l'ajoute
        menu = Menu.query.filter_by(nom=nom_menu).first()
        if menu:
            if not (menu in user.menus):
                user.menus.append(menu)  # On ajoute le menu créé à la table de l'utilisateur
                db.session.commit()
                return "Menu déjà existant. Il a été ajouté dans votre liste"
            else:
                return "[ERREUR] Vous possédez déjà ce menu dans votre liste."
        # Sinon, personne n'a encore créé ce menu, on va donc le créé et l'ajouté dans la bdd
        else:
            # ---- Ajout du menu dans la base de données ----
            if user and entree and plat and dessert:
                menu = Menu(entree_id=entree.id, plat_id=plat.id, dessert_id=dessert.id, nom=nom_menu)
                user.menus.append(menu)  # On ajoute le menu créé à la table de l'utilisateur
                db.session.commit()
                return "Menu non existant, il a été créé et ajouté à votre liste."
            else:
                return f"[ERREUR] : Une ou plusieurs informations ont été mal renseignées."

    # Avoir tous les menus de la bdd
    if request.method == "GET":
        all_menus = Menu.query.all()
        all_menus = [{"id": menu.id, "nom": menu.nom} for menu in all_menus]
        return jsonify(menus=all_menus)

    if request.method == "DELETE":
        req_json = request.json
        pseudo = req_json['Pseudo']
        nom = req_json['Nom_menu'].upper()
        menu = Menu.query.filter_by(nom=nom).first()
        user = User.query.filter_by(pseudo=pseudo).first()
        if menu and user:
            user.menus.remove(menu)
            db.session.commit()
            return "La recette " + nom + " a été supprimé des favoris."
        else:
            return "[ERREUR] : Les informations fournies sont incorrectes."

    else:
        # Retour méthodes prisent en charges
        return "[ERREUR] : Mauvaise méthode, POST et GET acceptés."


@views.route('/get-user-menus', methods=["GET"])
def get_user_menus():
    if request.method == "GET":
        req_json = request.json
        pseudo = req_json['Pseudo']
        user = User.query.filter_by(pseudo=pseudo).first()
        if user:
            liste_menus = [{
                "id": menu.id,
                "nom": menu.nom,
                "Entrée": (Recette.query.filter_by(id=menu.entree_id).first()).nom,
                "Plat": (Recette.query.filter_by(id=menu.plat_id).first()).nom,
                "Dessert": (Recette.query.filter_by(id=menu.dessert_id).first()).nom
            } for menu in user.menus]

            if user:
                return jsonify(user_menus=liste_menus)
            else:
                return "[ERREUR] : L'utilisateur ne possède pas de menus dans sa liste."
        else:
            return "[ERREUR] : L'utilisateur n'existe pas"

