# app/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from app.models import Usuario
from app import db

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    email    = data.get('email')
    password = data.get('password')
    nombre   = data.get('nombre')

    if not email or not password:
        return jsonify({'error': 'Email y password requeridos'}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': 'Email ya registrado'}), 400

    user = Usuario(nombre=nombre, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario creado', 'id': user.id}), 201

@bp_auth.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email    = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email y password requeridos'}), 400

    user = Usuario.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Credenciales inválidas'}), 401

    login_user(user)
    return jsonify({'mensaje': 'Inicio de sesión exitoso'}), 200

@bp_auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'mensaje': 'Sesión cerrada'}), 200
