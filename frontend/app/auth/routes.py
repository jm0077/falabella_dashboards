from flask import Blueprint, redirect, url_for, flash, session, current_app, render_template, request
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
import logging
from urllib.parse import urlencode
import json

auth_bp = Blueprint('auth', __name__)

# Ruta de login que redirige a Keycloak
@auth_bp.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))
    redirect_uri = url_for('auth.auth', _external=True, _scheme='https')
    keycloak = current_app.config['keycloak']  # Acceder a keycloak desde current_app
    return keycloak.authorize_redirect(redirect_uri)

# Ruta que maneja el callback de Keycloak y autentica al usuario
@auth_bp.route('/auth')
def auth():
    keycloak = current_app.config['keycloak']
    try:
        token = keycloak.authorize_access_token()
        userinfo = keycloak.userinfo(token=token)
    except Exception as e:
        logging.error(f"Error in authentication process: {str(e)}")
        flash("Failed to authenticate.", "error")
        return redirect(url_for('auth.login'))

    if not userinfo:
        flash("Failed to fetch user information.", "error")
        return redirect(url_for('auth.login'))

    # Autenticar al usuario con Flask-Login
    user_id = userinfo['sub']  # El 'sub' es el ID único del usuario en Keycloak
    user = User(user_id)
    login_user(user)

    # Guardar información del usuario en la sesión
    session['user'] = userinfo
    session['id_token'] = token.get('id_token')  # Guardar el ID token
    session['user_id'] = user_id

    # Redirigir al dashboard tras el inicio de sesión exitoso
    return redirect(url_for('auth.index'))

# Ruta de logout que también cierra sesión en Keycloak
@auth_bp.route('/logout')
@login_required
def logout():
    logging.info("Logout route accessed")
    keycloak = current_app.config['keycloak']
    logout_user()
    
    client_secrets = current_app.config.get('OIDC_CLIENT_SECRETS', {})
    if not client_secrets:
        logging.error("OIDC client secrets not found in app config")
        return redirect(url_for('auth.login'))

    keycloak_logout_url = f"{client_secrets.get('web', {}).get('issuer', '')}/protocol/openid-connect/logout"
    
    # Obtener el ID token de la sesión
    id_token = session.get('id_token')
    logging.info(f"ID token retrieved: {'Yes' if id_token else 'No'}")
    
    # Limpiar la sesión después de obtener el id_token
    session.clear()
    logging.info("Session cleared")
    
    # Usar la URL base de la aplicación como URI de redirección post-logout
    base_url = url_for('auth.login', _external=True, _scheme='https')

    # Construir los parámetros de la URL de cierre de sesión
    params = {
        'post_logout_redirect_uri': base_url,
        'client_id': client_secrets.get('web', {}).get('client_id', ''),
    }
    
    # Añadir id_token_hint si está disponible
    if id_token:
        params['id_token_hint'] = id_token

    # Construir la URL completa de cierre de sesión
    logout_url = f"{keycloak_logout_url}?{urlencode(params)}"

    logging.info(f"Redirecting to Keycloak logout URL: {logout_url}")
    return redirect(logout_url)

# Ruta principal que renderiza el contenido protegido con autenticación
@auth_bp.route('/')
@login_required
def index():
    # Redirigir al dashboard principal de Dash
    return redirect('/dashboard/')
