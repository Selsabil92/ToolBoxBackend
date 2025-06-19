from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.zap_service import run_zap

zap_bp = Blueprint("zap", __name__)

@zap_bp.route('/api/zap/scan', methods=['POST'])
@jwt_required()
def launch_zap_scan():
    data = request.get_json()
    target = data.get("target")

    if not target:
        return jsonify({"error": "Cible manquante"}), 400

    result = run_zap(target)
    return jsonify(result)
