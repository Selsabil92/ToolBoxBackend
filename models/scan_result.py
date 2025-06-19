from models import db
from datetime import datetime

class ScanResult(db.Model):
    __tablename__ = 'scan_results'

    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(255), nullable=False)
    tool = db.Column(db.String(50), nullable=False)  # nmap, hydra
    result = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, target, tool, result):
        self.target = target
        self.tool = tool
        self.result = result
