# app/dashboards/my_account/documents/upload/layout.py

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_upload_documents_layout():
    layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Carga de Documentos", className="mb-4"),
                html.P("Selecciona el banco y sube tu estado de cuenta en formato PDF.", className="mb-4"),
                dcc.Dropdown(  # Changed from dbc.Select to dcc.Dropdown
                    id="bank-selection",
                    options=[],  # Options will be filled dynamically
                    placeholder="Selecciona un banco",
                    className="mb-4"
                ),
                dcc.Upload(
                    id='upload-document',
                    children=html.Div([
                        'Arrastra y suelta o ',
                        html.A('selecciona un archivo PDF')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px 0'
                    },
                    multiple=False,
                    accept='application/pdf'
                ),
                html.Div(id='output-document-upload'),
                dbc.Button("Cargar", id="upload-button", color="primary", className="me-2 mt-3"),
                dbc.Button("Volver", href="/dashboard/my-account/documents/", color="secondary", className="mt-3"),
                dbc.Alert(id="flash-message", is_open=False, duration=4000, className="mt-3"),  # Moved inside the column for proper alignment
            ], md=10, lg=8, className="mx-auto")
        ], className="justify-content-center"),
        dcc.Loading(
            id="loading-upload",
            type="default",
            children=html.Div(id="loading-output-upload")
        ),
    ], fluid=True, className="py-4")

    return layout