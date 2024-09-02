import os
import secrets
import dash_bootstrap_components as dbc

BACKEND_ENDPOINT = "https://backend-falabella-app-service-alhjlx25pa-tl.a.run.app/api"
FLASK_SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(24))
DASH_ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
DASH_EXTERNAL_STYLESHEETS = [
    dbc.themes.BOOTSTRAP,
    f"{DASH_ASSETS_FOLDER}/css/styles.css",
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;700&display=swap'
]