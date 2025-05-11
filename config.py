import os

class Config:
    # Variables pour la base de données
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.environ.get('DB_USER', 'postgres')}:{os.environ.get('DB_PASSWORD', 'ToolBoxPentest')}@"
        f"{os.environ.get('DB_HOST', 'localhost')}:{os.environ.get('DB_PORT', 5433)}/{os.environ.get('DB_NAME', 'toolbox')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Désactive le suivi des modifications pour économiser des ressources

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'ToolBoxPentestSecure')  # Clé secrète pour signer les tokens JWT
