from flask import Blueprint, jsonify
from models.log import Log

logs_bp = Blueprint('logs', __name__)

@logs_bp.route('/all', methods=['GET'])
def get_logs():
    logs = Log.query.all()
    return jsonify([log.to_dict() for log in logs]), 200
