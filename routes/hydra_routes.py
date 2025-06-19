from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.hydra import run_hydra_scan

hydra_bp = Blueprint('hydra', __name__)

@hydra_bp.route('/api/hydra/attack', methods=['POST'])
@jwt_required()
def hydra_attack():
    try:
        data = request.get_json()
        target = data.get('target')
        service = data.get('service')
        port = data.get('port')  # facultatif
        wordlist = data.get('wordlist')  # facultatif
        userlist = data.get('userlist')  # facultatif

        if not target or not service:
            return jsonify({"success": False, "error": "Paramètres requis : target et service"}), 400

        result = run_hydra_scan(target, service, wordlist, userlist, port)
        return jsonify({
            "success": True,
            "target": target,
            "service": service,
            "output": result
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Erreur lors de l'exécution : {str(e)}"}), 500
