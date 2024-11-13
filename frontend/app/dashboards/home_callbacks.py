# app/dashboards/home_callbacks.py
import requests
from dash.dependencies import Input, Output
from flask_login import current_user
from config import CARDS_API_ENDPOINT
from .home_layout import (
    create_error_layout,
    create_first_time_layout,
    create_no_documents_layout,
    create_default_layout
)

def get_user_estado(user_id):
    """
    Obtiene el estado del usuario desde la API
    """
    try:
        response = requests.get(f"{CARDS_API_ENDPOINT}/usuario-estado", params={"userId": user_id})
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error getting user status: {str(e)}")
        return None

def register_home_callbacks(app):
    @app.callback(
        Output('user-status-store', 'data'),
        Input('url', 'pathname')
    )
    def fetch_user_status(pathname):
        """
        Obtiene el estado del usuario cuando se carga la página
        """
        if not current_user or not current_user.is_authenticated:
            return None
            
        return get_user_estado(current_user.id)

    @app.callback(
        Output('home-content', 'children'),
        Input('user-status-store', 'data')
    )
    def update_home_content(user_status):
        """
        Actualiza el contenido de la página principal basado en el estado del usuario
        """
        if user_status is None:
            return create_error_layout()
            
        if user_status['primer_ingreso']:
            return create_first_time_layout()
            
        if not user_status['primer_ingreso'] and not user_status['documento_cargado']:
            return create_no_documents_layout()
            
        return create_default_layout()