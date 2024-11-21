# app/dashboards/my_account/documents/download/layout.py

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_download_documents_layout():
    layout = dbc.Container([
        # Añade dcc.Download
        dcc.Download(id="download-trigger"),
        
        # El resto de tu layout permanece igual
        dbc.Row([
            dbc.Col([
                html.H2("Descarga de Documentos", className="mb-4"),
                html.P("Selecciona el banco y el documento a descargar.", className="mb-4"),
                
                # Bank selection dropdown
                dcc.Dropdown(
                    id="bank-selection-download",
                    options=[],
                    placeholder="Selecciona un banco",
                    className="mb-4"
                ),
                
                # Documents list dropdown
                dcc.Dropdown(
                    id="documents-list",
                    options=[],
                    placeholder="Selecciona un documento",
                    className="mb-4"
                ),
                
                # Buttons
                dbc.Button(
                    "Descargar",
                    id="download-button",
                    color="primary",
                    className="me-2 mt-3",
                    disabled=True
                ),
                dbc.Button(
                    "Volver",
                    href="/dashboard/my-account/documents/",
                    color="secondary",
                    className="mt-3"
                ),
                
                # Alert for messages
                dbc.Alert(
                    id="documents-alert",
                    is_open=False,
                    duration=4000,
                    className="mt-3"
                ),
            ], md=10, lg=8, className="mx-auto")
        ], className="justify-content-center"),
        
        # Loading spinner
        dcc.Loading(
            id="loading-download",
            type="default",
            children=html.Div(id="loading-output-download")
        ),
    ], fluid=True, className="py-4")

    return layout