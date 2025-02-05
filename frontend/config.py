import os
import secrets
import dash_bootstrap_components as dbc

BACKEND_ENDPOINT = "https://backend-falabella-app-service-913912993840.southamerica-west1.run.app/api"
FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(24))
DASH_ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), 'app', 'static')
DASH_EXTERNAL_STYLESHEETS = [
    dbc.themes.BOOTSTRAP,
    '/static/css/styles.css',
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css'
]

# Configuraciones adicionales
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'
FLASK_HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.environ.get('FLASK_PORT', 8080))

# Configuración de Flask-Login
LOGIN_DISABLED = False

# Configuración de Keycloak OpenID Connect
OIDC_CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
OIDC_SCOPES = ['openid', 'email', 'profile']
CLIENT_SCOPE = 'manage-users'

# Nuevo endpoint para la API de tarjetas
CARDS_API_ENDPOINT = "https://backend-tarjetas-service-913912993840.southamerica-west1.run.app/api"

# Configuración del bucket de GCS
GCS_BUCKET_NAME = 'account-statements-customers-northern-hope-449920-t0'