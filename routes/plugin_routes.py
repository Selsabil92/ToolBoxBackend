from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
import os
import importlib.util

plugin_bp = Blueprint('plugin_bp', __name__)
PLUGIN_DIR = os.path.join(os.path.dirname(__file__), '..', 'plugins')

@plugin_bp.route('/api/plugins/list', methods=['GET'])
@jwt_required()
def list_plugins():
    try:
        plugins = [
            f.replace('.py', '')
            for f in os.listdir(PLUGIN_DIR)
            if f.endswith('.py') and not f.startswith('__')
        ]
        return jsonify(plugins)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@plugin_bp.route('/api/plugins/run/<plugin_name>', methods=['GET'])
@jwt_required()
def run_plugin(plugin_name):
    plugin_path = os.path.join(PLUGIN_DIR, f"{plugin_name}.py")

    if not os.path.isfile(plugin_path):
        return jsonify({"error": f"Plugin '{plugin_name}' not found"}), 404

    try:
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, 'run'):
            return jsonify({"error": f"Plugin '{plugin_name}' does not have a 'run()' function"}), 400

        output = module.run()
        return jsonify({
            "plugin": plugin_name,
            "output": output
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

