from flask import current_app, session
from flask_login import UserMixin
import requests
import logging
from config import CLIENT_SCOPE

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        self.first_name = None
        self.last_name = None
        self.email = None
        self.load_user_info()

    def load_user_info(self):
        userinfo = session.get('user', {})
        self.first_name = userinfo.get('given_name')
        self.last_name = userinfo.get('family_name')
        self.email = userinfo.get('email')

    @staticmethod
    def get(user_id):
        return User(user_id)

    def update(self, first_name=None, last_name=None, email=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email:
            self.email = email

        keycloak = current_app.config['keycloak']
        client_secrets = current_app.config.get('OIDC_CLIENT_SECRETS')

        if not client_secrets:
            logging.error("OIDC client secrets not found in app config")
            return False, "Error en la configuración del servidor"

        # Obtener el token de acceso del servicio
        token_url = f"{client_secrets['web']['issuer']}/protocol/openid-connect/token"
        client_id = client_secrets['web']['client_id']
        client_secret = client_secrets['web']['client_secret']

        token_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }

        try:
            token_response = requests.post(token_url, data=token_data, verify='/etc/ssl/certs/ca-certificates.crt')
            token_response.raise_for_status()
            service_token = token_response.json()['access_token']
        except requests.RequestException as e:
            logging.error(f"Error obtaining service account token: {str(e)}")
            return False, "Error al obtener el token de servicio"

        headers = {
            'Authorization': f'Bearer {service_token}',
            'Content-Type': 'application/json'
        }

        user_data = {
            'firstName': self.first_name,
            'lastName': self.last_name,
            'email': self.email
        }

        admin_url = client_secrets['web']['issuer'].replace('/realms/master', '')
        update_url = f"{admin_url}/admin/realms/master/users/{self.id}"

        try:
            response = requests.put(update_url, json=user_data, headers=headers, verify='/etc/ssl/certs/ca-certificates.crt')
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Error updating user info in Keycloak: {str(e)}")
            return False, f"Error al actualizar la información: {str(e)}"

        session['user'] = {
            'sub': self.id,
            'given_name': self.first_name,
            'family_name': self.last_name,
            'email': self.email
        }

        return True, "Información actualizada correctamente"