from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)

# Nouvelle route correcte pour récupérer les utilisateurs en JSON
@auth_bp.route("/users", methods=["GET"])
def show_users():
    users = User.query.all()  # Récupère tous les utilisateurs de la BDD
    users_list = [{"id": user.id, "username": user.username} for user in users]

    # Retourner les utilisateurs en JSON
    return jsonify(users_list), 200

# Route d'enregistrement avec traitement des données (POST)
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(force=True)

    # Vérifier si l'utilisateur existe déjà
    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "User already exists"}), 400

    # Hacher le mot de passe et créer l'utilisateur
    hashed_password = generate_password_hash(data["password"])
    new_user = User(username=data["username"], password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201  # Retourne un message de succès

# Route de login avec authentification JWT
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if user and check_password_hash(user.password, data["password"]):
        # Générer un token JWT
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token, "message": "Login successful"}), 200

    return jsonify({"message": "Invalid credentials"}), 401
