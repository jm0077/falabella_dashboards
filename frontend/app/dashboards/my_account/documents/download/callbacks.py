# app/dashboards/my_account/documents/download/callbacks.py

from dash import Input, Output, State, callback_context, html, dcc
from dash.exceptions import PreventUpdate
import requests
from flask_login import current_user
from google.cloud import storage
import dash_bootstrap_components as dbc
from config import CARDS_API_ENDPOINT, GCS_BUCKET_NAME
import re
from datetime import datetime, timedelta
import logging
import os
from google.oauth2 import service_account

MONTHS = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
          "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Credenciales para la cuenta de servicio
creds = service_account.Credentials.from_service_account_file(
    'SecretData/quick-bonfire-441017-v2-20ceb2642aa5.json'
)

# Crea el cliente de Storage con las credenciales
storage_client = storage.Client(credentials=creds)


def register_download_callbacks(app):
    @app.callback(
        Output("bank-selection-download", "options"),
        Input("url", "pathname")
    )
    def load_banks_download(pathname):
        try:
            if pathname != "/dashboard/my-account/documents/download/":
                raise PreventUpdate

            logger.info(f"Loading banks for user {current_user.id}")
            user_id = current_user.id
            api_url = f"{CARDS_API_ENDPOINT}/usuario-bancos?userId={user_id}"

            response = requests.get(api_url)
            response.raise_for_status()
            user_banks = response.json()

            logger.debug(f"Retrieved {len(user_banks)} banks for user {user_id}")

            options = [
                {
                    "label": html.Img(
                        src=f"/static/img/{bank['banco_nombre'].lower().replace(' ', '_')}_logo.svg",
                        height="30px"
                    ),
                    "value": bank['banco_nombre']
                }
                for bank in user_banks
            ]
            return options

        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in load_banks_download: {str(e)}")
            return []

    @app.callback(
        [
            Output("documents-list", "options"),
            Output("documents-list", "value"),
            Output("download-button", "disabled"),
            Output("documents-alert", "children"),
            Output("documents-alert", "is_open"),
            Output("documents-alert", "color")
        ],
        [Input("bank-selection-download", "value")],
        [State("documents-list", "value")]
    )
    def list_processed_documents(selected_bank, selected_document):
        try:
            if not selected_bank:
                logger.debug("No bank selected")
                return [], None, True, "Selecciona un banco para continuar.", True, "warning"

            logger.info(f"Listing documents for bank: {selected_bank}, user: {current_user.id}")
            bucket = storage_client.bucket(GCS_BUCKET_NAME)
            user_id = current_user.id
            prefix = f"{user_id}/{selected_bank}/Step4_Processed/"

            logger.debug(f"Searching for documents with prefix: {prefix}")
            blobs = list(bucket.list_blobs(prefix=prefix))
            logger.debug(f"Found {len(blobs)} total blobs")

            pdf_files = [blob for blob in blobs if blob.name.lower().endswith('.pdf')]
            logger.debug(f"Found {len(pdf_files)} PDF files")

            if not pdf_files:
                return [], None, True, "No se encontraron documentos para este banco.", True, "warning"

            def extract_year_month(filename):
                # Extrae el mes y año del nombre del archivo
                match = re.search(r'(\w+)-(\d{4})\.pdf', filename)
                if match:
                    return (int(match.group(2)), MONTHS.index(match.group(1)) + 1)
                return (0, 0)

            sorted_files = sorted(
                pdf_files,
                key=lambda x: extract_year_month(x.name.split('/')[-1]),
                reverse=True
            )

            document_options = [
                {
                    "label": blob.name.split('/')[-1].replace('.pdf', ''),
                    "value": blob.name
                }
                for blob in sorted_files
            ]

            logger.debug(f"Generated {len(document_options)} document options")
            return document_options, None, False, "", False, "success"

        except Exception as e:
            error_msg = f"Error al listar documentos: {str(e)}"
            logger.error(error_msg)
            return [], None, True, error_msg, True, "danger"

    @app.callback(
        [
            Output("documents-alert", "children", allow_duplicate=True),
            Output("documents-alert", "is_open", allow_duplicate=True),
            Output("documents-alert", "color", allow_duplicate=True),
            Output("download-trigger", "data")
        ],
        [Input("download-button", "n_clicks")],
        [State("documents-list", "value")],
        prevent_initial_call=True
    )
    def download_document(n_clicks, selected_document):
        if not n_clicks:
            raise PreventUpdate

        if not selected_document:
            logger.warning("Download attempted without document selection")
            return "Selecciona un documento para descargar.", True, "warning", ""

        try:
            logger.info(f"Generating download URL for document: {selected_document}")
            bucket = storage_client.bucket(GCS_BUCKET_NAME)
            blob = bucket.blob(selected_document)

            # Descargar el contenido del blob
            document_content = blob.download_as_bytes()

            # Obtener el nombre del archivo
            filename = selected_document.split('/')[-1]

            logger.info(f"Successfully prepared document for download: {filename}")
            return "Descarga iniciada...", True, "success", dcc.send_bytes(document_content, filename)

        except Exception as e:
            error_msg = f"Error al generar la URL de descarga: {str(e)}"
            logger.error(error_msg)
            return error_msg, True, "danger", None