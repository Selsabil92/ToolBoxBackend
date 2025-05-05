from flask import Blueprint, request, jsonify
from models.scan_result import ScanResult
from models import db
from services.scan_nmap import scan_nmap
from flask_jwt_extended import jwt_required
from routes.decorators import admin_required  # Import du décorateur admin_required
from models.scan_result import ScanResult

# Blueprint pour les routes de scan
scan_bp = Blueprint('scan', __name__)

# Route pour lancer un scan Nmap
@scan_bp.route('/nmap', methods=['POST'])
@jwt_required()  # Vérifie que l'utilisateur a un token valide
@admin_required  # Restreint l'accès aux admins seulement
def nmap_scan():
    # Récupération des données du corps de la requête
    data = request.get_json()
    target = data.get('target')

    # Validation de la cible
    if not target:
        return jsonify({'error': 'Target is required'}), 400

    # Lancer le scan Nmap
    result = scan_nmap(target)

    # Sauvegarder le résultat du scan dans la base de données
    scan_entry = ScanResult(
        target=target,
        result=result,
        tool='nmap'  # Nom de l'outil utilisé
    )
    db.session.add(scan_entry)
    db.session.commit()

    # Retourner les résultats du scan
    return jsonify({'result': result}), 200
