from flask import Blueprint, jsonify
from services.scan_hydra import run_hydra_scan

hydra_bp = Blueprint('hydra', __name__)

@hydra_bp.route('/attack', methods=['POST'])
def hydra_attack():
    data = request.get_json()
    result = run_hydra_scan(data['target'], data['service'], data['wordlist'])
    return jsonify({'result': result}), 200
