# app/__init__.py

from dotenv import load_dotenv
load_dotenv()  # carga .env antes de importar Config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from sqlalchemy import MetaData

from config import Config

# 1) Definimos metadata con esquema por defecto 'public'
metadata = MetaData(schema="public")

# 2) Creamos la extensión SQLAlchemy usando ese metadata
db = SQLAlchemy(metadata=metadata)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 3) Inicializamos extensiones
    db.init_app(app)
    CORS(app)
    login_manager.init_app(app)

    # 4) Registro de usuario para Flask-Login
    from app.models import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # 5) Registramos blueprints
    from app.routes.auth     import bp_auth
    from app.routes.usuarios import usuarios_bp

    app.register_blueprint(bp_auth,     url_prefix='/auth')
    app.register_blueprint(usuarios_bp, url_prefix='/api/usuarios')

    return app
