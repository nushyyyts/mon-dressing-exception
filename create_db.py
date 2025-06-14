# create_db.py
import os
from app import app, db, User, Item # Importe l'instance 'app' et 'db', et tes modèles depuis app.py

# Assurez-vous que l'application est configurée pour le développement local
# Cela est important si le root_path est défini de manière spécifique dans app.py
# et que vous voulez que la BDD soit créée à la racine de votre projet local.
# Cette logique est déjà dans app.py, mais on s'assure que ce script utilise le bon chemin
# pour la création de la BDD, quel que soit l'environnement où il est exécuté.
if os.environ.get('RENDER'):
    # Si ce script est exécuté directement sur Render (via Build Command),
    # app.root_path sera déjà '/opt/render/project/src' si app.py est à jour.
    # On s'assure juste que la DB est créée au bon endroit.
    db_path = os.path.join('/opt/render/project/src', 'site.db')
else:
    # Pour le développement local, la DB sera à la racine du projet
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

print("Chemin de la base de données pour la création :", app.config['SQLALCHEMY_DATABASE_URI'])

with app.app_context():
    print("Création de toutes les tables de la base de données...")
    db.create_all()
    print("Tables créées avec succès (ou déjà existantes) !")