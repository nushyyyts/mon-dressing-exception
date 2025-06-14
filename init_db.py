# init_db.py
import os
from app import app, db, User, Item # Assurez-vous que User et Item sont importés si db.create_all en a besoin

print("Début de l'initialisation de la base de données sur Render...")

# Assurez-vous que le chemin racine est correct pour Render lors de ce script
# C'est déjà géré dans app.py, mais on le reconfirme ici
if os.environ.get('RENDER'):
    app.root_path = '/opt/render/project/src'
else:
    app.root_path = os.path.dirname(os.path.abspath(__file__)) # Pour une exécution locale de ce script

# Redéfinit SQLALCHEMY_DATABASE_URI pour être certain qu'il pointe vers le site.db attendu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'site.db')

with app.app_context():
    print("Tentative de création des tables...")
    db.create_all()
    print("Tables créées (ou déjà existantes) !")