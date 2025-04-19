from flask import Blueprint, jsonify
from services.memory_analysis import analyze_memory

memory_bp = Blueprint('memory', __name__)

@memory_bp.route('/analyze', methods=['GET'])
def analyze():
    result = analyze_memory()
    return jsonify({'result': result}), 200
