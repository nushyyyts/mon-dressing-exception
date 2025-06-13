from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import uuid # Pour générer des noms de fichiers uniques
from werkzeug.utils import secure_filename # Pour sécuriser les noms de fichiers


app = Flask(__name__)

# --- Configuration de l'Application ---
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# CLÉ SECRÈTE : CHANGEZ CELA ABSOLUMENT POUR UNE CHAÎNE LONGUE ET ALÉATOIRE !
app.config['SECRET_KEY'] = 'UNE_NOUVELLE_CLE_SECRETE_TRES_FORTE_POUR_LA_PRODUCTION'

# Configuration pour les téléchargements de fichiers
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # Limite de 16MB pour les fichiers

db = SQLAlchemy(app)

# --- Modèles de Base de Données ---

# Modèle Utilisateur
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    items = db.relationship('Item', backref='owner', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return '<User %r>' % self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modèle : Article (Vêtement/Pièce de Collection)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    condition = db.Column(db.String(50), nullable=True)
    is_rare = db.Column(db.Boolean, default=False, nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default_item.jpg')
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

# --- Fonctions utilitaires pour les téléchargements de fichiers ---
def save_picture(picture):
    if picture:
        random_hex = str(uuid.uuid4())[:8]
        _, f_ext = os.path.splitext(picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path, 'static', 'uploads', picture_fn)
        picture.save(picture_path)
        return picture_fn
    return None

# --- Routes de l'Application ---

@app.route('/')
def index():
    featured_items = Item.query.order_by(Item.date_added.desc()).limit(4).all()
    featured_showcases = []
    seen_users = set()
    for item in featured_items:
        if item.owner.username not in seen_users:
            featured_showcases.append(item.owner)
            seen_users.add(item.owner.username)
        if len(featured_showcases) >= 4:
            break
            
    return render_template('index.html', featured_showcases=featured_showcases)


@app.route('/explorer')
def explorer():
    all_users_with_items = User.query.join(Item).group_by(User.id).all()
    return render_template('explorer.html', all_users_with_items=all_users_with_items)


@app.route('/my-showcase', methods=['GET', 'POST'])
def my_showcase():
    if 'user_id' not in session:
        flash('Vous devez être connecté pour accéder à votre vitrine.', 'info')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    
    # Gérer l'ajout d'article
    if request.method == 'POST' and 'item-name' in request.form:
        name = request.form['item-name']
        description = request.form['item-description']
        category = request.form['item-category']
        year = request.form['item-year']
        condition = request.form['item-condition']
        is_rare = 'is-rare' in request.form

        image_file = request.files.get('item-image')
        item_image_filename = save_picture(image_file)

        try:
            new_item = Item(
                name=name,
                description=description,
                category=category,
                year=int(year) if year else None,
                condition=condition,
                is_rare=is_rare,
                image_file=item_image_filename if item_image_filename else 'default_item.jpg',
                owner=user
            )
            db.session.add(new_item)
            db.session.commit()
            flash('Article ajouté avec succès !', 'success')
            return redirect(url_for('my_showcase'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de l\'ajout de l\'article : {e}', 'error')

    user_items = Item.query.filter_by(user_id=user.id).order_by(Item.date_added.desc()).all()
    rare_items_count = Item.query.filter_by(user_id=user.id, is_rare=True).count()
    
    return render_template(
        'my-showcase.html',
        username=user.username,
        user_items=user_items,
        total_items_count=len(user_items),
        rare_items_count=rare_items_count,
        views_count='5.2K',
        comments_count='32'
    )

# Route pour la suppression d'un article
@app.route('/my-showcase/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if 'user_id' not in session:
        flash('Vous devez être connecté pour supprimer un article.', 'danger')
        return redirect(url_for('login'))

    item = Item.query.get_or_404(item_id)

    if item.user_id != session['user_id']:
        flash('Vous n\'êtes pas autorisé à supprimer cet article.', 'error')
        return redirect(url_for('my_showcase'))

    if item.image_file and item.image_file != 'default_item.jpg':
        try:
            os.remove(os.path.join(app.root_path, 'static', 'uploads', item.image_file))
        except OSError as e:
            print(f"Erreur lors de la suppression de l'image : {e}")
            flash('Erreur lors de la suppression de l\'image.', 'warning')

    db.session.delete(item)
    db.session.commit()
    flash('Article supprimé avec succès !', 'success')
    return redirect(url_for('my_showcase'))


# Route pour la modification d'un article (GET pour afficher le formulaire, POST pour soumettre)
@app.route('/my-showcase/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if 'user_id' not in session:
        flash('Vous devez être connecté pour modifier un article.', 'info')
        return redirect(url_for('login'))

    item = Item.query.get_or_404(item_id)

    if item.user_id != session['user_id']:
        flash('Vous n\'êtes pas autorisé à modifier cet article.', 'error')
        return redirect(url_for('my_showcase'))

    if request.method == 'POST':
        item.name = request.form['item-name']
        item.description = request.form['item-description']
        item.category = request.form['item-category']
        item.year = int(request.form['item-year']) if request.form['item-year'] else None
        item.condition = request.form['item-condition']
        item.is_rare = 'is-rare' in request.form

        image_file = request.files.get('item-image')
        if image_file and image_file.filename != '':
            if item.image_file and item.image_file != 'default_item.jpg':
                try:
                    os.remove(os.path.join(app.root_path, 'static', 'uploads', item.image_file))
                except OSError as e:
                    print(f"Erreur lors de la suppression de l'ancienne image : {e}")
            item_image_filename = save_picture(image_file)
            item.image_file = item_image_filename if item_image_filename else 'default_item.jpg'

        try:
            db.session.commit()
            flash('Article mis à jour avec succès !', 'success')
            return redirect(url_for('my_showcase'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la mise à jour de l\'article : {e}', 'error')

    return render_template('my-showcase.html', 
                           username=item.owner.username, 
                           item_to_edit=item,
                           user_items=item.owner.items,
                           total_items_count=len(item.owner.items),
                           rare_items_count=Item.query.filter_by(user_id=item.user_id, is_rare=True).count(),
                           views_count='5.2K',
                           comments_count='32')


# Route pour la page de vitrine d'un utilisateur spécifique
@app.route('/user-showcase/<username>')
def user_showcase(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash(f'La vitrine de "{username}" n\'existe pas.', 'error')
        return redirect(url_for('explorer'))
    
    user_items = Item.query.filter_by(user_id=user.id).order_by(Item.date_added.desc()).all()
    user_rare_items_count = Item.query.filter_by(user_id=user.id, is_rare=True).count()

    return render_template('user-showcase.html', 
                           target_username=user.username,
                           user_items=user_items,
                           user_rare_items_count=user_rare_items_count)


# Route pour la page de détail d'un article - NOUVELLE ROUTE
@app.route('/item/<int:item_id>')
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item_detail.html', item=item)


# Route pour la connexion et l'inscription
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'username_login' in request.form:
            username = request.form['username_login']
            password = request.form['password_login']
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['username'] = user.username
                flash('Connexion réussie ! Bienvenue.', 'success')
                return redirect(url_for('my_showcase'))
            else:
                flash('Nom d\'utilisateur ou mot de passe incorrect.', 'error')
        elif 'username_register' in request.form:
            username = request.form['username_register']
            email = request.form['email_register']
            password = request.form['password_register']
            confirm_password = request.form['confirm_password_register']
            if password != confirm_password:
                flash('Les mots de passe ne correspondent pas.', 'error')
            elif User.query.filter_by(username=username).first():
                flash('Ce nom d\'utilisateur est déjà pris.', 'error')
            elif User.query.filter_by(email=email).first():
                flash('Cet email est déjà enregistré.', 'error')
            else:
                new_user = User(username=username, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
                return redirect(url_for('login', form='login'))
                
    form_to_show = request.args.get('form', 'login')
    return render_template('login.html', form_to_show=form_to_show)

# Route pour la déconnexion
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('index'))


# --- Lancement de l'Application ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)