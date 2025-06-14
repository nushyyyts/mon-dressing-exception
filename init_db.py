# init_db.py
import os
from app import app, db, User, Item # Assurez-vous que User et Item sont importés si db.create_all en a besoin

print("Début de l'initialisation de la base de données sur Render...")

# Assurez-vous que le chemin racine est correct pour Render lors de ce script
# C'est déjà géré dans app.py, mais on le reconfirme ici pour l'exécution directe via Build Command
if os.environ.get('RENDER'):
    # Si ce script est exécuté directement sur Render (via Build Command),
    # app.root_path sera déjà '/opt/render/project/src' si app.py est à jour.
    # On s'assure juste que la DB est créée au bon endroit.
    db_path = os.path.join('/opt/render/project/src', 'site.db')
else:
    # Pour le développement local, la DB sera à la racine du projet
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site.db')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

with app.app_context():
    print("Tentative de création des tables...")
    db.create_all()
    print("Tables créées (ou déjà existantes) !")