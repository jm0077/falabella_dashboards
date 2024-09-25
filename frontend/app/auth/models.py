from flask_login import UserMixin
from flask import current_app, session

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
        user = User(user_id)
        return user

    def update(self, first_name=None, last_name=None, email=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if email:
            self.email = email
        
        # Aquí deberías implementar la lógica para actualizar la información del usuario en Keycloak
        # Por ejemplo:
        # keycloak = current_app.config['keycloak']
        # access_token = session.get('access_token')
        # user_data = {
        #     'firstName': self.first_name,
        #     'lastName': self.last_name,
        #     'email': self.email
        # }
        # keycloak.update_user(self.id, user_data, access_token)
        
        # Actualizar la información en la sesión
        session['user'] = {
            'sub': self.id,
            'given_name': self.first_name,
            'family_name': self.last_name,
            'email': self.email
        }