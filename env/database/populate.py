from models.user import User
from app import app, db

with app.app_context():
    user = User(email='selsabil.guennouni@supdevinci-edu.fr', password_hash='hashed_password')
    db.session.add(user)
    db.session.commit()
