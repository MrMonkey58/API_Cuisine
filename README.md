# API_Cuisine
Projet option SIN I2 2023/2024 - UniLasalle Amiens

## 📖 Table des Matières

1. [Aperçu](#-aperçu)
2. [Fonctionnement générale](#-fonctionnement-générale)
3. [Installation](#-installation)
4. [Utilisation](#-utilisation)
5. [Code source](#%EF%B8%8F-code-source)
6. [Auteurs](#%EF%B8%8F-auteurs)


## 📋 Aperçu

Cette API a pour but d'être utilisée pour la création de recettes de cuisine par des utilisateurs.

**Différentes possibilités s'offrent à eux :**
1. **Créer une recette**
2. **Créer et ajouter un ingrédient**
3. **Créer et ajouter une recette**
   - Avec les quantités de chaque ingrédient
   - Des instructions détaillées
4. **Ajouter une recette dans ses favoris**
5. **Créer et ajouter des menus**
   - Entrée
   - Plat
   - Dessert

L'utilisateur a bien sûr la possibilité de supprimer et voir ses modifications. Vous pouvez pour cela utiliser les méthodes GET, POST ou DEL avec les URLs des requêtes correspondantes.
La documentation qui suit montrera comment générer et utiliser ces requêtes.


## 🔧 Fonctionnement générale

Toute l'API reçoit des informations via le format JSON (pour plus d'infomations sur cette notation, se rendre sur : [https://www.json.org/json-en.html](https://www.json.org/json-en.html) .
Nous avons utilisé le langage de programmation python pour notre projet et les modules Flask et Flask-sqlalchemy. 
En effet, une base de donnée est créée pour stocker dans ses tables toutes les informations (Utilisateurs, Ingrédients, Reccettes (instructions, quantités, ...).


## 🚀 Installation

Utilisez Python version: 3.10


**Hiérarchie à respecter :**

    📦Projet_Cuisine
    ┣ 📂instance
    ┃ ┗ 📜database.db
    ┣ 📂website
    ┃ ┗ 📜init.py
    ┃ ┗ 📜models.py
    ┃ ┗ 📜routes.py
    ┣ 📜main.py

    
Bibliothèques utilisées : Flask, OS, SQLAlchemy

Flask: [https://flask.palletsprojects.com/en/3.0.x/](https://flask.palletsprojects.com/en/3.0.x/)

OS: [https://docs.python.org/fr/3/library/os.html](https://docs.python.org/fr/3/library/os.html)

SQLAlchemy: [https://www.sqlalchemy.org](https://www.sqlalchemy.org)


1. **Installer Flask :**
    ```bash
    pip install Flask
    ```

2. **Installer OS (si nécessaire) :**
    ```bash
    pip install os
    ```

3. **Installer SQLAlchemy :**
    ```bash
    pip install SQLAlchemy
    ```



## 💡 Utilisation

Pour utiliser l'API, référez vous a la documentation technique fournie ci-joint:
[Documentation technique Postman](https://documenter.getpostman.com/view/30304133/2s9YXib2av)

## ⌨️ Code source

Le code source peut être améliorer selon vos besoins. Pour cela prenez connaissance des informations suivantes.

Code respectant au mieux la norme "PEP8".

Utilisation des notations :
    - PascalCase pour les classes
    - snake_case pour les fonctions



## 🙋‍♂️ Auteurs

Ce projet a été co-créé par :

- **MARTIN Tom**
  - 📧 Email: [tom.martin@etu.unilasalle.fr](mailto:tom.martin@etu.unilasalle.fr)

- **TRIVES VAN BOXSTAEL Arthur**
  - 📧 Email: [arthur.trives-vanboxstael@etu.unilasalle.fr](mailto:arthur.trives-vanboxstael@etu.unilasalle.fr)


