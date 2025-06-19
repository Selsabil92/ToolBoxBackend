# routes/parallel_plugins.py

import os
import importlib.util
import concurrent.futures
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

parallel_plugins_bp = Blueprint('parallel_plugins', __name__)

PLUGINS_DIR = "plugins"

def load_plugin(plugin_name):
    plugin_path = os.path.join(PLUGINS_DIR, f"{plugin_name}.py")
    if not os.path.exists(plugin_path):
        raise FileNotFoundError(f"Plugin '{plugin_name}' not found.")
    spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

@parallel_plugins_bp.route('/api/plugins/run/parallel', methods=['POST'])
@jwt_required()
def run_plugins_parallel():
    data = request.get_json()
    plugin_names = data.get("plugins", [])

    results = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(plugin_names)) as executor:
        futures = {
            name: executor.submit(load_plugin(name).run) for name in plugin_names
        }

        for name, future in futures.items():
            try:
                results[name] = future.result(timeout=300)
            except Exception as e:
                results[name] = {"error": str(e)}

    return jsonify(results)
