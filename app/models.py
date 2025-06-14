from flask_login import UserMixin
from . import db

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True)
    usuarios = db.relationship('Usuario', back_populates='rol')

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    google_id = db.Column(db.String(200), unique=True, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    rol = db.relationship('Rol', back_populates='usuarios')
