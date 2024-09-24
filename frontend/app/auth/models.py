from flask_login import UserMixin
from flask import current_app

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        self.first_name = None
        self.last_name = None
        self.email = None

    @staticmethod
    def get(user_id):
        oauth = current_app.config['oauth']
        keycloak = current_app.config['keycloak']
        user = User(user_id)
        try:
            userinfo = keycloak.userinfo()
            user.first_name = userinfo.get('given_name')
            user.last_name = userinfo.get('family_name')
            user.email = userinfo.get('email')
        except Exception as e:
            current_app.logger.error(f"Error fetching user info: {str(e)}")
        return user

    def update(self, first_name=None, last_name=None, email=None):
        # Aquí deberías implementar la lógica para actualizar la información del usuario en Keycloak
        # Por ahora, solo actualizamos los atributos locales
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email:
            self.email = email