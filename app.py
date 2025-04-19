import sys
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Ajoute le chemin du projet au path pour éviter les erreurs d'import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Chargement des routes
from routes.auth import auth_bp  # auth_bp est le blueprint dans routes/auth.py
from routes.scan import scan_bp 

# Configuration & utilitaires
from models import db  # db est défini dans models/__init__.py

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Création de l'application Flask
app = Flask(__name__)

# Configuration de la base de données (PostgreSQL si défini, sinon SQLite par défaut)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///toolbox.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration de la clé JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Sécurité CORS (uniquement autorisé depuis localhost:3000 pour le frontend)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Initialisation des extensions
db.init_app(app)
jwt = JWTManager(app)

# Créer les tables dans la base PostgreSQL si elles n'existent pas
with app.app_context():
    db.create_all()

# Enregistrement des blueprints des routes
app.register_blueprint(auth_bp, url_prefix='/auth')  
app.register_blueprint(scan_bp, url_prefix='/scan')


# Route de test
@app.route('/')
def accueil():
    return "Bienvenue dans l'application Toolbox Pentest 🛠️💻🔐"

# Route favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True, port=5000)
