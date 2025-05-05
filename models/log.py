# models/log.py
import logging
from models import db
from datetime import datetime

# Modèle de log pour la base de données
class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, message, level):
        self.message = message
        self.level = level

# Configuration du logger standard
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Définir les fonctions de log
def log_info(message):
    logger.info(message)
    log = Log(message=message, level='INFO')
    db.session.add(log)
    db.session.commit()

def log_error(message):
    logger.error(message)
    log = Log(message=message, level='ERROR')
    db.session.add(log)
    db.session.commit()
