# app/__init__.py

import os
from dotenv import load_dotenv

# 1) Carga variables de entorno ANTES de importar Config
load_dotenv()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config  # ahora sí verá DATABASE_URL

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    from app.routes.usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

    return app
