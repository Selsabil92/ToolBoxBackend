import sys
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate
from models.log import log_info, log_error

# Ajoute le chemin du projet au path pour éviter les erreurs d'import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Chargement des routes
from routes.auth import auth_bp  # auth_bp est le blueprint dans routes/auth.py
from routes.scan import scan_bp 

# Configuration & utilitaires
from models import db  # db est défini dans models/__init__.py
from models.log import log_info, log_error  # Import des fonctions de logging

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Création de l'application Flask
app = Flask(__name__)

# Configuration de la base de données (PostgreSQL si défini, sinon SQLite par défaut)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///toolbox.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration de la clé JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Assure-toi que cette clé est définie dans .env

# Configuration de CORS (uniquement autorisé depuis localhost:3000 pour le frontend)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Initialisation des extensions
db.init_app(app)
jwt = JWTManager(app)

# Gestion des migrations de base de données avec Flask-Migrate
migrate = Migrate(app, db)

# Enregistrement des blueprints des routes
app.register_blueprint(auth_bp, url_prefix='/auth')  
app.register_blueprint(scan_bp, url_prefix='/scan')

# Route de test
@app.route('/')
def accueil():
    log_info("Accès à la route d'accueil")
    return "Bienvenue dans l'application Toolbox Pentest 🛠️💻🔐"

# Route favicon
@app.route('/favicon.ico')
def favicon():
    log_info("Accès à la favicon")
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Gestion des erreurs en mode développement
@app.errorhandler(500)
def internal_error(error):
    log_error(f"Erreur interne: {str(error)}")
    if app.config["ENV"] == "production":
        return jsonify({"message": "Something went wrong. Please try again later."}), 500
    return jsonify({"message": str(error)}), 500

@app.errorhandler(404)
def not_found_error(error):
    log_error(f"Page non trouvée: {str(error)}")
    return jsonify({"message": "Resource not found."}), 404

# Ajouter des headers de sécurité à chaque réponse
@app.after_request
def apply_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# Lancement de l'application
if __name__ == "__main__":
    app.run(debug=True, port=5000)
