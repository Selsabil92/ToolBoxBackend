# delete_all_users.py
from app import app
from models import db, User

with app.app_context():
    confirmation = input("⚠️ Cette action va supprimer TOUS les utilisateurs. Continuer ? (oui/non) : ").strip().lower()

    if confirmation == 'oui':
        users = User.query.all()
        for user in users:
            db.session.delete(user)
        db.session.commit()
        print(f"✅ Tous les utilisateurs ({len(users)}) ont été supprimés.")
    else:
        print("❌ Opération annulée.")
