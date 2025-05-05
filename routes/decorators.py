from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify

# Décorateur pour vérifier si l'utilisateur est un admin
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Récupère le rôle de l'utilisateur dans les claims du JWT
        claims = get_jwt_identity()
        if claims.get('role') != 'admin':
            return jsonify({"message": "Access forbidden: Admins only"}), 403
        return fn(*args, **kwargs)
    return wrapper
