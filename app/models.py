# app/models.py
from flask_login import UserMixin
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class Rol(db.Model):
    __tablename__ = 'roles'
    id      = db.Column(db.Integer, primary_key=True)
    nombre  = db.Column(db.String(50), unique=True)
    usuarios = db.relationship('Usuario', back_populates='rol')

class Usuario(UserMixin, db.Model):
    __tablename__   = 'usuarios'
    id              = db.Column(db.Integer, primary_key=True)
    nombre          = db.Column(db.String(100))
    email           = db.Column(db.String(120), unique=True, nullable=False)
    password_hash   = db.Column(db.Text, nullable=False)
    rol_id          = db.Column(db.Integer, db.ForeignKey('roles.id'))
    rol             = db.relationship('Rol', back_populates='usuarios')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol.nombre if self.rol else None
        }
