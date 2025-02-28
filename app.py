from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
from config_app import Config
from routes.auth_routes import auth_bp
from routes.scan_routes import scan_bp
from database import db
from middleware import register_error_handlers
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from models import User

load_dotenv()  # Charger les variables d'environnement depuis le fichier .env

# Initialisation de l'application Flask
app = Flask(__name__)
app.config.from_object(Config)

# Activer CORS pour autoriser les requêtes du frontend React
CORS(app)  # Permet à l'application d'accepter les requêtes de n'importe quelle origine

# Initialisation des extensions
db.init_app(app)  # L'initialisation de db doit être faite après la configuration de l'application
jwt = JWTManager(app)

# Crée la base de données et les tables
with app.app_context():
    db.create_all()

# Fonction pour ajouter ou mettre à jour un utilisateur
def add_or_update_user(username, password):
    # Vérifier si l'utilisateur existe déjà
    existing_user = User.query.filter_by(username=username).first()

    if not existing_user:
        # Si l'utilisateur n'existe pas, l'ajouter
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        print(f"Utilisateur '{username}' ajouté à la base de données")
    else:
        # Si l'utilisateur existe, mettre à jour son mot de passe
        existing_user.password = generate_password_hash(password)
        db.session.commit()
        print(f"Mot de passe de '{username}' mis à jour")

# Route pour la suppression d'un utilisateur
@app.route('/auth/delete_user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({"message": "Username is required"}), 400

    user_to_delete = User.query.filter_by(username=username).first()

    if user_to_delete:
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({"message": f"Utilisateur '{username}' supprimé avec succès"}), 200
    else:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

# Route pour la page d'accueil
@app.route('/')
def home():
    return "Bienvenue sur l'API ToolBox Pentest🕵️‍♂️💻🔐"

# Route pour le favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Enregistrement des blueprints (routes)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(scan_bp, url_prefix='/scan')
print(app.url_map)

# Gestion des erreurs
register_error_handlers(app)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
