from flask import Blueprint, request, jsonify
from models.user import User
from utils.validators import validate_email

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not validate_email(data['email']):
        return jsonify({'message': 'Invalid email'}), 400

    user = User(email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201
