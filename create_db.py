# create_db.py
import os
from app import app, db, User, Item # Importe l'instance 'app' et 'db', et tes modèles depuis app.py

# Assurez-vous que l'application est configurée pour le développement local
# Cela est important si le root_path est défini de manière spécifique dans app.py
# et que vous voulez que la BDD soit créée à la racine de votre projet local.
if os.environ.get('RENDER'):
    # Si vous exécutez ce script directement sur Render, la configuration sera prise en compte.
    pass
else:
    # Pour le développement local, assurez-vous que basedir est le chemin correct
    app.root_path = os.path.dirname(os.path.abspath(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'site.db')


print("Chemin de la base de données :", app.config['SQLALCHEMY_DATABASE_URI'])

with app.app_context():
    print("Création de toutes les tables de la base de données...")
    db.create_all()
    print("Tables créées avec succès !")