from flask import Blueprint, request, jsonify 
from models.user import User
from utils.crypto import generate_jwt
from utils.validators import validate_email  

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    # 🔍 Validation de l'email
    if not validate_email(email):
        return jsonify({'message': 'Invalid email format'}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        token = generate_jwt(user)
        return jsonify({'token': token}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401
