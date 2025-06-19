import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Charge les variables du .env
load_dotenv()

# Récupère la clé
FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise ValueError("❌ FERNET_KEY manquante dans le fichier .env")

fernet = Fernet(FERNET_KEY.encode())

def encrypt_data(plaintext: str) -> str:
    return fernet.encrypt(plaintext.encode()).decode()

def decrypt_data(ciphertext: str) -> str:
    return fernet.decrypt(ciphertext.encode()).decode()
