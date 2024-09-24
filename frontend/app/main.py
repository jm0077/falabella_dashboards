from flask import Flask, redirect, url_for
from flask_login import LoginManager, login_required, logout_user
from dash import Dash
from config import FLASK_SECRET_KEY, DASH_ASSETS_FOLDER, DASH_EXTERNAL_STYLESHEETS, OIDC_CLIENT_SECRETS
from .dashboards.dashboard_factory import create_dashboards
from .auth_setup import setup_oauth
import json
import logging

def create_app():
    server = Flask(__name__)
    server.config['SECRET_KEY'] = FLASK_SECRET_KEY
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Cargar los secretos del cliente OIDC
    with open(OIDC_CLIENT_SECRETS) as f:
        server.config['OIDC_CLIENT_SECRETS'] = json.load(f)

    # Configurar OAuth usando auth_setup
    oauth, keycloak = setup_oauth(server)

    # Almacenar oauth y keycloak en la configuración de la app para usarlos en otros lugares
    server.config['oauth'] = oauth
    server.config['keycloak'] = keycloak

    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(server)
    login_manager.login_view = 'auth.login'  # Usar el Blueprint para la vista de login

    # Cargar la sesión de usuario
    @login_manager.user_loader
    def load_user(user_id):
        from app.auth.models import User
        return User(user_id)

    # Registrar Blueprint de autenticación
    from app.auth.routes import auth_bp
    server.register_blueprint(auth_bp, url_prefix='/auth')  # Mantener el prefijo '/auth'
							 
    app = Dash(
        __name__,
        server=server,
        url_base_pathname='/dashboard/',
        assets_folder=DASH_ASSETS_FOLDER,
        external_stylesheets=DASH_EXTERNAL_STYLESHEETS,
        suppress_callback_exceptions=True
    )

    # Crear y registrar dashboards
    create_dashboards(app)

    # Añadir una ruta para la raíz que redirija a /dashboard/
    @server.route('/')
    def index():
        return redirect('/dashboard/')

    return server, app

server, app = create_app()

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080, debug=False)