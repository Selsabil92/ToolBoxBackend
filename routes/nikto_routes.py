from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.nikto_service import run_nikto_scan

nikto_bp = Blueprint('nikto', __name__)

@nikto_bp.route('/api/nikto/scan', methods=['POST'])
@jwt_required()
def scan_nikto():
    data = request.get_json()
    target = data.get('target')

    if not target:
        return jsonify({"error": "Cible manquante"}), 400

    result = run_nikto_scan(target, verbose=True)

    if result["status"] == "error":
        return jsonify(result), 500

    return jsonify(result), 200
