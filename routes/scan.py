from flask import Blueprint, request, jsonify
from models import db
from models.scan_result import ScanResult
from services.scan_nmap import scan_nmap
# from services.scan_hydra import scan_hydra  # à ajouter quand dispo
# from services.scan_openvas import scan_openvas  # à ajouter quand dispo
from flask_jwt_extended import jwt_required
from routes.decorators import admin_required

# Blueprint pour les routes de scan
scan_bp = Blueprint('scan', __name__)

# Route pour lancer un scan Nmap
@scan_bp.route('/nmap', methods=['POST'])
@jwt_required()
@admin_required
def nmap_scan():
    data = request.get_json()
    target = data.get('target')

    if not target:
        return jsonify({'error': 'Target is required'}), 400

    result = scan_nmap(target)

    scan_entry = ScanResult(
        target=target,
        tool='nmap',
        result=result
    )
    db.session.add(scan_entry)
    db.session.commit()

    return jsonify({'result': result}), 200


# Route future pour Hydra
@scan_bp.route('/hydra', methods=['POST'])
@jwt_required()
@admin_required
def hydra_scan():
    return jsonify({'message': 'Hydra scan endpoint prêt, script à intégrer'}), 200


# Route future pour OpenVAS
@scan_bp.route('/openvas', methods=['POST'])
@jwt_required()
@admin_required
def openvas_scan():
    return jsonify({'message': 'OpenVAS scan endpoint prêt, script à intégrer'}), 200
