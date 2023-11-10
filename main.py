# main.py

"""
Projet option SIN I2 2023/2024 - UniLasalle Amiens

Créateurs:
    - MARTIN Tom
    - TRIVES VAN BOXSTAEL Arthur


Application réalisée en fichiers multiples:
    - main.py
    - __init__.py
    - models.py
    - routes.py
    - database.db

Projet réalisé en Python, le projet a pour objectif de construire une application destinée à fournir des recettes de
cuisine pour différents utilisateurs.

Code respectant au mieux la norme "PEP8".

Bibliothèques utilisées : Flask, OS, SQLAlchemy ;

Utilisation des notations :
                          - PascalCase pour les classes
                          - snake_case pour les fonctions

Lien GitHub de l'API : https://github.com/MrMonkey58/API_Cuisine
"""


# Imports
from Website import create_app

app = create_app()

# Démarage de l'application
if __name__ == "__main__":
    app.run(debug=True)
