# routes/enum_parallel_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import concurrent.futures

from services.wireshark_service import run as wireshark_run
from services.dirbuster_service import run as dirbuster_run
from services.enum4linux_service import run as enum4linux_run
from services.nikto_service import run as nikto_run
from services.gobuster_service import run as gobuster_run

enum_parallel_bp = Blueprint("enum_parallel", __name__, url_prefix="/api/enum")

tool_map = {
    "wireshark": wireshark_run,
    "dirbuster": dirbuster_run,
    "enum4linux": enum4linux_run,
    "nikto": nikto_run,
    "gobuster": gobuster_run
}

@enum_parallel_bp.route('/parallel', methods=['POST'])
@jwt_required()
def run_enum_parallel():
    data = request.get_json()
    target = data.get("target")
    tools = data.get("tools", [])

    if not target or not tools:
        return jsonify({"message": "Cible ou outils manquants"}), 400

    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(tools)) as executor:
        futures = {
            tool: executor.submit(tool_map[tool], target)
            for tool in tools if tool in tool_map
        }

        for tool, future in futures.items():
            try:
                results[tool] = future.result(timeout=60)
            except Exception as e:
                results[tool] = {"error": str(e)}

    return jsonify(results)
