# app/dashboards/home_callbacks.py
import requests
from dash.dependencies import Input, Output
from flask_login import current_user
from config import CARDS_API_ENDPOINT
from .home_layout import (
    create_error_layout,
    create_first_time_layout,
    create_no_banks_layout,
    create_no_documents_layout,
    create_default_layout
)
from datetime import datetime

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

def get_user_banks(user_id):
    """
    Obtiene los bancos del usuario desde la API
    """
    try:
        response = requests.get(f"{CARDS_API_ENDPOINT}/usuario-bancos", params={"userId": user_id})
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error getting user banks: {str(e)}")
        return []

def update_user_estado(user_id, primer_ingreso, fecha_primer_ingreso=None):
    """
    Actualiza el estado del usuario a través de la API
    """
    try:
        response = requests.put(f"{CARDS_API_ENDPOINT}/usuario-estado", json={
            "userId": user_id,
            "primer_ingreso": primer_ingreso,
            "fecha_primer_ingreso": fecha_primer_ingreso.isoformat() if fecha_primer_ingreso else None
        })
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error updating user status: {str(e)}")
        return None

def register_home_callbacks(app):
    @app.callback(
        [Output('user-status-store', 'data'),
         Output('user-status-updated', 'data')],
        Input('url', 'pathname')
    )
    def fetch_user_status(pathname):
        """
        Obtiene el estado del usuario cuando se carga la página
        """
        if not current_user or not current_user.is_authenticated:
            return None, None
            
        user_status = get_user_estado(current_user.id)
        
        # Verificar si es el primer ingreso y actualizar el estado del usuario
        user_status_updated = user_status.copy()
        if user_status and user_status['primer_ingreso']:
            user_status_updated['primer_ingreso'] = False
            
        return user_status, user_status_updated

    @app.callback(
        Output('home-content', 'children'),
        [Input('user-status-store', 'data'),
         Input('user-status-updated', 'data')])
    def update_home_content(user_status, user_status_updated):
        """
        Actualiza el contenido de la página principal basado en el estado del usuario
        """
        if user_status is None:
            return create_error_layout()
            
        # Actualizar el estado del usuario si es necesario
        if user_status_updated['primer_ingreso'] != user_status['primer_ingreso']:
            update_user_estado(
                current_user.id,
                primer_ingreso=user_status_updated['primer_ingreso'],
                fecha_primer_ingreso=datetime.now()
            )
            
        # Verificar si es el primer ingreso
        if user_status['primer_ingreso']:
            return create_first_time_layout()
        
        # Obtener bancos del usuario
        user_banks = get_user_banks(current_user.id)
        
        # Verificar si tiene bancos habilitados
        banks_enabled = any(bank.get('habilitado', False) for bank in user_banks)
        
        # Si no tiene bancos habilitados, mostrar layout para habilitar bancos
        if not banks_enabled:
            return create_no_banks_layout()
        
        # Si llega aquí, mostrar dashboard por defecto
        return create_default_layout()