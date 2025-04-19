from flask import Blueprint, request, jsonify
from models.scan_result import ScanResult
from models import db
from services.scan_nmap import scan_nmap

scan_bp = Blueprint('scan', __name__)

@scan_bp.route('/nmap', methods=['POST'])
def nmap_scan():
    data = request.get_json()
    target = data.get('target')

    if not target:
        return jsonify({'error': 'Target is required'}), 400

    result = scan_nmap(target)

    scan_entry = ScanResult(
        target=target,
        result=result,
        tool='nmap'  # ← ici le champ est bien reconnu
    )
    db.session.add(scan_entry)
    db.session.commit()

    return jsonify({'result': result}), 200
