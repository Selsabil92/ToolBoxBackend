from flask import Blueprint, request, jsonify
from models.user import User
from utils.validators import validate_email
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, get_jwt
)
from routes.decorators import admin_required  # Pour les routes réservées aux admins

auth_bp = Blueprint('auth', __name__)

# Login utilisateur
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    if not validate_email(email):
        return jsonify({'message': 'Invalid email format'}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # Ajoute le rôle de l'utilisateur dans le token
        access_token = create_access_token(
            identity=user.id,
            additional_claims={"role": user.role}
        )
        return jsonify({
            'token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role
            }
        }), 200

    return jsonify({'message': 'Invalid credentials'}), 401


# 👤 Exemple de route protégée avec JWT simple (pour un utilisateur connecté)
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user:
        return jsonify({
            'id': user.id,
            'email': user.email,
            'role': user.role
        }), 200

    return jsonify({'message': 'User not found'}), 404


# Route réservée aux admins
@auth_bp.route('/admin-dashboard', methods=['GET'])
@jwt_required()
@admin_required
def admin_dashboard():
    return jsonify({"message": "Welcome to the admin dashboard!"}), 200
