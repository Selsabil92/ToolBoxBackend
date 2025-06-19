from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.ssh_config import ssh_connect_and_execute
from services.hydra import run_hydra_scan
from services.meta import run_metasploit
from services.zap_service import run_zap
from services.wireshark_service import run as run_wireshark
from services.enum4linux_service import run as run_enum4linux
from services.vuln_service import scan_vulnerabilities

import os
import json
from datetime import datetime

scans = Blueprint('scans', __name__)

@scans.route('/api/scans/execute', methods=['POST'])
@jwt_required()
def execute_scan():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    target_ip = data.get('target_ip')
    scan_type = data.get('scan_type')
    service = data.get('service')  # 🔥 Nouveau champ utilisé pour Hydra

    if not target_ip or not scan_type:
        return jsonify({"status": "error", "message": "Missing target_ip or scan_type"}), 400

    scan_output = None
    try:
        if scan_type == "nmap":
            command = f"nmap -sV {target_ip}"
            scan_output = ssh_connect_and_execute(command, '127.0.0.1', 'root', '/root/.ssh/toolbox_key')

        elif scan_type == "openvas":
            command = f"openvas-cli --target {target_ip}"
            scan_output = ssh_connect_and_execute(command, '127.0.0.1', 'root', '/root/.ssh/toolbox_key')

        elif scan_type == "metasploit":
            scan_output = run_metasploit(target_ip)

        elif scan_type == "hydra":
            if not service:
                return jsonify({"status": "error", "message": "Le champ 'service' est requis pour Hydra"}), 400
            scan_output = run_hydra_scan(target_ip, service=service)

        elif scan_type == "zap":
            scan_output = run_zap(target_ip)

        elif scan_type == "wireshark":
            scan_output = run_wireshark(target_ip)

        elif scan_type == "enum4linux":
            scan_output = run_enum4linux(target_ip)

        elif scan_type == "vuln-analysis":
            scan_output = scan_vulnerabilities(target_ip)
            filename = scan_output.get("saved_as", "").split("/")[-1]
        else:
            return jsonify({"status": "error", "message": f"Unsupported scan type: {scan_type}"}), 400

        if scan_type != "vuln-analysis":
            os.makedirs("uploads/scans", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            target_safe = target_ip.replace(".", "_")
            filename = f"{scan_type}_result_{target_safe}_{timestamp}.json"
            file_path = os.path.join("uploads/scans", filename)

            report_data = {
                "target": target_ip,
                "scan_type": scan_type,
                "scan_output": scan_output,
                "created_at": datetime.now().isoformat(),
                "status": "Disponible",
                "user_id": current_user_id
            }

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=4)

        return jsonify({
            "scan_output": scan_output,
            "report_filename": filename
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erreur pendant le scan : {str(e)}"
        }), 500
