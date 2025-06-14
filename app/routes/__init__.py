import os
from dotenv import load_dotenv
load_dotenv()  # 📥 carga .env antes de usar Config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # ruta de login

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    login_manager.init_app(app)

    # importa para user_loader
    from app.models import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # registra blueprints
    from app.routes.auth import bp_auth
    from app.routes.usuarios import usuarios_bp

    app.register_blueprint(bp_auth, url_prefix='/auth')
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

    return app
