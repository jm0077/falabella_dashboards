from flask import Flask
from flask_login import LoginManager
from dash import Dash
from config import FLASK_SECRET_KEY, DASH_ASSETS_FOLDER, DASH_EXTERNAL_STYLESHEETS
from .auth.routes import auth_bp
from .auth.models import User
from .dashboards.dashboard_factory import create_dashboards

def create_app():
    server = Flask(__name__)
    server.config['SECRET_KEY'] = FLASK_SECRET_KEY

    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(server)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    # Registrar blueprints
    server.register_blueprint(auth_bp)

    # Crear instancia de Dash
    app = Dash(
        __name__,
        server=server,
        url_base_pathname='/dashboard/',
        assets_folder=DASH_ASSETS_FOLDER,
        external_stylesheets=DASH_EXTERNAL_STYLESHEETS
    )

    # Crear y registrar dashboards
    create_dashboards(app)

    return server, app

server, app = create_app()

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=8080, debug=False)