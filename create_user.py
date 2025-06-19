from getpass import getpass
from werkzeug.security import generate_password_hash
from models import db, User
from app import app

def create_user():
    with app.app_context():
        username = input("Nom d'utilisateur : ")
        email = input("Adresse email : ")
        password = getpass("Mot de passe : ")
        password_hash = generate_password_hash(password)

        user = User(username=username, email=email, password=password_hash)
        db.session.add(user)
        db.session.commit()
        print("✅ Utilisateur créé avec succès.")

if __name__ == '__main__':
    create_user()
