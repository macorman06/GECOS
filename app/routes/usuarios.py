from flask import Blueprint, request, jsonify
from app.models import db, Usuario, Rol

usuarios_bp = Blueprint('usuarios_bp', __name__)

@usuarios_bp.route('/', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        'id': u.id,
        'nombre': u.nombre,
        'email': u.email,
        'rol': u.rol.nombre if u.rol else None
    } for u in usuarios])

@usuarios_bp.route('/', methods=['POST'])
def crear_usuario():
    data = request.json
    nuevo = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        rol_id=data.get('rol_id')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Usuario creado", "id": nuevo.id}), 201
