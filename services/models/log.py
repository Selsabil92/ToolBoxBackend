# 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modèle de log
class Log(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    level = db.Column(db.String(50), nullable=False)  # Par exemple: 'INFO', 'ERROR'
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, message, level):
        self.message = message
        self.level = level
