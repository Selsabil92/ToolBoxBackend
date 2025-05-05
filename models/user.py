from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Modèle de l'utilisateur
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # Par défaut : 'user'

    def __init__(self, username, email, password, role='user'):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)  # Hachage du mot de passe
        self.role = role

    def check_password(self, password):
        # Vérifie si le mot de passe fourni correspond au mot de passe haché
        return check_password_hash(self.password, password)

