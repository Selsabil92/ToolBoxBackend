import sys
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_migrate import Migrate

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from models import db
from models.log import log_info, log_error
from routes.auth import auth_bp
from routes.scan import scan_bp

# Charger les variables d'environnement
load_dotenv()

# Flask App
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///toolbox.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["CELERY_BROKER_URL"] = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
app.config["CELERY_RESULT_BACKEND"] = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

# Extensions
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Celery
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"]
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

# Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(scan_bp, url_prefix='/scan')

@app.route('/')
def accueil():
    log_info("Accès à la route d'accueil")
    return "Bienvenue dans l'application Toolbox Pentest 🛠️💻🔐"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(500)
def internal_error(error):
    log_error(f"Erreur interne: {str(error)}")
    return jsonify({"message": "Internal server error"}), 500

@app.errorhandler(404)
def not_found_error(error):
    log_error(f"Page non trouvée: {str(error)}")
    return jsonify({"message": "Resource not found"}), 404

@app.after_request
def apply_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

with app.app_context():
    db.create_all()
    log_info("Base de données initialisée")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
