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
        self.dni = None
        self.load_user_info()

    def load_user_info(self):
        userinfo = session.get('user', {})
        self.first_name = userinfo.get('given_name')
        self.last_name = userinfo.get('family_name')
        self.email = userinfo.get('email')
        self.dni = userinfo.get('dni')

    @staticmethod
    def get(user_id):
        return User(user_id)

    def update(self, first_name=None, last_name=None, email=None, dni=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email:
            self.email = email
        if dni:
            self.dni = dni

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
            'email': self.email,
            'attributes': {
                'dni': [self.dni] if self.dni else []
            }
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
            'email': self.email,
            'dni': self.dni
        }

        return True, "Información actualizada correctamente"

    def update_password(self, current_password, new_password):
        keycloak = current_app.config['keycloak']
        client_secrets = current_app.config.get('OIDC_CLIENT_SECRETS')

        if not client_secrets:
            logging.error("OIDC client secrets not found in app config")
            return False, "Error en la configuración del servidor"

        token_url = f"{client_secrets['web']['issuer']}/protocol/openid-connect/token"
        client_id = client_secrets['web']['client_id']
        client_secret = client_secrets['web']['client_secret']

        # Primero, verificamos la contraseña actual
        verify_data = {
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': self.email,
            'password': current_password
        }

        try:
            verify_response = requests.post(token_url, data=verify_data, verify='/etc/ssl/certs/ca-certificates.crt')
            if verify_response.status_code != 200:
                return False, "La contraseña actual es incorrecta"
        except requests.RequestException as e:
            logging.error(f"Error verifying current password: {str(e)}")
            return False, "Error al verificar la contraseña actual"

        # Si la verificación es exitosa, procedemos a cambiar la contraseña
        # Obtenemos un token de acceso para el cliente
        token_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }

        try:
            token_response = requests.post(token_url, data=token_data, verify='/etc/ssl/certs/ca-certificates.crt')
            token_response.raise_for_status()
            access_token = token_response.json()['access_token']
        except requests.RequestException as e:
            logging.error(f"Error obtaining access token: {str(e)}")
            return False, "Error al obtener el token de acceso"

        # Cambiamos la contraseña usando la API de administración
        admin_url = client_secrets['web']['issuer'].replace('/realms/master', '')
        change_password_url = f"{admin_url}/admin/realms/master/users/{self.id}/reset-password"

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        password_data = {
            'type': 'password',
            'value': new_password,
            'temporary': False
        }

        try:
            response = requests.put(change_password_url, json=password_data, headers=headers, verify='/etc/ssl/certs/ca-certificates.crt')
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Error changing password in Keycloak: {str(e)}")
            return False, f"Error al cambiar la contraseña: {str(e)}"

        return True, "Contraseña actualizada correctamente"