from flask import Blueprint, request, jsonify 
from models.user import User
from utils.validators import validate_email  
from flask_jwt_extended import create_access_token, jwt_required
from routes.decorators import admin_required  # Import du décorateur

# Blueprint d'authentification
auth_bp = Blueprint('auth', __name__)

# Route de login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    # Validation de l'email
    if not validate_email(email):
        return jsonify({'message': 'Invalid email format'}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        # 🔐 Génération du token JWT avec le rôle
        access_token = create_access_token(
            identity=user.id,
            additional_claims={"role": user.role}
        )
        return jsonify({'token': access_token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# Exemple de route protégée pour les admins (utilisation du décorateur)
@auth_bp.route('/admin-dashboard', methods=['GET'])
@jwt_required()  # Vérifie le token
@admin_required  # Vérifie que l'utilisateur a le rôle admin
def admin_dashboard():
    return jsonify({"message": "Welcome to the admin dashboard!"}), 200
