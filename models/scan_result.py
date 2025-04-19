from models import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON

class ScanResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(255), nullable=False)
    result = db.Column(JSON, nullable=False)
    tool = db.Column(db.String(50), default='nmap')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


