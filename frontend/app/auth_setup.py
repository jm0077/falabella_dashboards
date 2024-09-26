import os
from authlib.integrations.flask_client import OAuth
import json
from config import OIDC_CLIENT_SECRETS, OIDC_SCOPES, CLIENT_SCOPE
import logging
from requests.exceptions import RequestException
import requests

def setup_oauth(app):
    oauth = OAuth(app)
    
    with open(OIDC_CLIENT_SECRETS) as f:
        client_secrets = json.load(f)
    
    logging.info(f"Attempting to connect to Keycloak at: {client_secrets['web']['issuer']}")
    
    # Configurar la sesión de requests para usar el certificado
    session = requests.Session()
    session.verify = '/etc/ssl/certs/ca-certificates.crt'
    
    try:
        keycloak = oauth.register(
            name='keycloak',
            client_id=client_secrets['web']['client_id'],
            client_secret=client_secrets['web']['client_secret'],
            server_metadata_url=f"{client_secrets['web']['issuer']}/.well-known/openid-configuration",
            client_kwargs={
                'scope': ' '.join(OIDC_SCOPES),  # Añadimos CLIENT_SCOPE aquí
                'timeout': 30
            },
            # Añadir estas líneas para configurar correctamente la autenticación
            authorize_params={
                'response_type': 'code',
            },
            userinfo_endpoint=f"{client_secrets['web']['issuer']}/protocol/openid-connect/userinfo"
        )
        # Configurar la sesión después de registrar el cliente
        keycloak.session = session
        logging.info("Keycloak registration successful")
    except RequestException as e:
        logging.error(f"Network error when registering Keycloak: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error registering Keycloak: {str(e)}")
        raise
    
    return oauth, keycloak