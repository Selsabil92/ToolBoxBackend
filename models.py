from datetime import datetime, timedelta
import jwt 
from flask import current_app
from database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def generate_token(self):
        # Génère un token JWT avec la clé secrète
        token = jwt.encode({
            'username': self.username,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token
