import os
import requests
from flask import (
    Blueprint, redirect, url_for, session,
    request, current_app, abort
)
from urllib.parse import urlencode
from app.utils.oauth import get_google_provider_cfg
from app import db
from app.models import Usuario
from flask_login import login_user, logout_user, login_required

bp_auth = Blueprint('auth', __name__)

@bp_auth.route('/login')
def login():
    cfg = get_google_provider_cfg(current_app.config['GOOGLE_DISCOVERY_URL'])
    auth_endpoint = cfg['authorization_endpoint']
    params = {
        'client_id':     current_app.config['GOOGLE_CLIENT_ID'],
        'redirect_uri':  url_for('auth.callback', _external=True),
        'scope':         'openid email profile',
        'response_type': 'code',
        'hd':            current_app.config['GOOGLE_ALLOWED_DOMAIN'],
        # opcionalmente state, access_type...
    }
    return redirect(f"{auth_endpoint}?{urlencode(params)}")


@bp_auth.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        abort(400, "No se recibió código de autorización")

    cfg = get_google_provider_cfg(current_app.config['GOOGLE_DISCOVERY_URL'])
    token_endpoint = cfg['token_endpoint']

    token_resp = requests.post(
        token_endpoint,
        data={
            'code':          code,
            'client_id':     current_app.config['GOOGLE_CLIENT_ID'],
            'client_secret': current_app.config['GOOGLE_CLIENT_SECRET'],
            'redirect_uri':  url_for('auth.callback', _external=True),
            'grant_type':    'authorization_code'
        },
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    token_json = token_resp.json()
    if 'access_token' not in token_json:
        abort(400, "Error al obtener token de Google")

    userinfo_endpoint = cfg['userinfo_endpoint']
    userinfo_resp = requests.get(
        userinfo_endpoint,
        headers={'Authorization': f"Bearer {token_json['access_token']}"}
    )
    userinfo = userinfo_resp.json()

    # Verifica dominio corporativo
    if userinfo.get('email_verified') and userinfo.get('hd') == current_app.config['GOOGLE_ALLOWED_DOMAIN']:
        uid   = userinfo['sub']
        email = userinfo['email']
        name  = userinfo['name']

        # Busca o crea el usuario en tu BD
        user = Usuario.query.filter_by(google_id=uid).first()
        if not user:
            user = Usuario(nombre=name, email=email, google_id=uid)
            db.session.add(user)
            db.session.commit()

        # Inicia sesión
        login_user(user)
        return redirect(url_for('usuarios_bp.listar_usuarios'))
    else:
        abort(403, "Usuario no autorizado en este dominio")


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    return "Sesión cerrada", 200
