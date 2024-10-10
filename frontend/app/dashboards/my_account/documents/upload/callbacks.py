# app/dashboards/my_account/documents/upload/callbacks.py

from dash import Input, Output, State, callback_context, html, ALL, no_update
from dash.exceptions import PreventUpdate
import requests
import dash_bootstrap_components as dbc
from flask_login import current_user
from google.cloud import storage
import base64
from config import CARDS_API_ENDPOINT, GCS_BUCKET_NAME

def register_upload_callbacks(app):
    @app.callback(
        Output("bank-selection", "options"),
        Input("url", "pathname")
    )
    def load_banks(pathname):
        if pathname != "/dashboard/my-account/documents/upload/":
            raise PreventUpdate

        user_id = current_user.id
        api_url = f"{CARDS_API_ENDPOINT}/usuario-bancos?userId={user_id}"

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            user_banks = response.json()

            options = [
                {
                    "label": html.Img(src=f"/static/img/{bank['banco_nombre'].lower().replace(' ', '_')}_logo.svg", height="30px"),
                    "value": bank['banco_nombre']
                }
                for bank in user_banks
            ]

            return options

        except requests.RequestException as e:
            return []

    @app.callback(
        Output("output-document-upload", "children"),
        Output("flash-message", "children"),
        Output("flash-message", "is_open"),
        Output("flash-message", "color"),
        Output("upload-document", "contents"),
        Input("upload-document", "contents"),
        State("upload-document", "filename"),
    )
    def update_output(content, filename):
        if content is None:
            raise PreventUpdate

        if not filename.lower().endswith('.pdf'):
            return (
                None,
                "Por favor, sube un archivo PDF.",
                True,
                "danger",
                None  # Clear the upload contents
            )

        return (
            html.Div(f"Archivo seleccionado: {filename}"),
            None,
            False,
            None,
            no_update
        )

    @app.callback(
        Output("loading-output-upload", "children"),
        Output("bank-selection", "value"),
        Output("upload-document", "contents", allow_duplicate=True),
        Output("flash-message", "children", allow_duplicate=True),
        Output("flash-message", "is_open", allow_duplicate=True),
        Output("flash-message", "color", allow_duplicate=True),
        Output("output-document-upload", "children", allow_duplicate=True),
        Input("upload-button", "n_clicks"),
        State("upload-document", "contents"),
        State("upload-document", "filename"),
        State("bank-selection", "value"),
        prevent_initial_call=True
    )
    def upload_document(n_clicks, content, filename, selected_bank):
        if n_clicks is None or content is None:
            raise PreventUpdate

        ctx = callback_context
        if not ctx.triggered:
            raise PreventUpdate

        if not selected_bank:
            return None, no_update, no_update, "Por favor, selecciona un banco antes de cargar el documento.", True, "danger", no_update

        if not filename.lower().endswith('.pdf'):
            return None, no_update, no_update, "Por favor, sube un archivo PDF.", True, "danger", no_update

        try:
            # Decodificar el contenido del archivo
            content_type, content_string = content.split(',')
            decoded = base64.b64decode(content_string)

            # Configurar el cliente de Google Cloud Storage
            storage_client = storage.Client()
            bucket = storage_client.bucket(GCS_BUCKET_NAME)

            # Crear la ruta del archivo en el bucket
            user_id = current_user.id
            file_path = f"{user_id}/{selected_bank}/Step0_Input/{filename}"

            # Subir el archivo al bucket
            blob = bucket.blob(file_path)
            blob.upload_from_string(decoded, content_type='application/pdf')

            return None, None, None, "Documento cargado exitosamente.", True, "success", None  # Clear the selected file display

        except Exception as e:
            return None, no_update, no_update, f"Error al cargar el documento: {str(e)}", True, "danger", no_update