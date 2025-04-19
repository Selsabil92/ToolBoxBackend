from werkzeug.security import generate_password_hash

password = 'projetcyber'
hashed = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

print(f"🔐 Mot de passe hashé : {hashed}")
