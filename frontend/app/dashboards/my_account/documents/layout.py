# app/dashboards/my_account/documents/layout.py

from dash import html
import dash_bootstrap_components as dbc

def create_documents_layout():
    document_options = [
        {"title": "Cargar Documentos", "description": "Sube tus estados de cuenta y otros documentos importantes", "icon": "documentos.svg", "href": "/dashboard/my-account/documents/upload/"},
        {"title": "Consulta de Documentos", "description": "Revisa y descarga tus documentos almacenados", "icon": "documentos.svg", "href": "#"},
    ]

    document_cards = [
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.A([
                        html.Div([
                            html.Img(src=f"/static/img/my-account/{option['icon']}", className="account-icon"),
                            html.Div([
                                html.H5(option['title'], className="card-title"),
                                html.P(option['description'], className="card-text"),
                            ], className="card-content"),
                            html.Img(src="/static/img/my-account/flecha.svg", className="account-arrow")
                        ], className="d-flex align-items-center justify-content-between")
                    ], href=option['href'], className="text-decoration-none text-reset")
                ]),
                className="h-100 account-card",
            ),
            md=6,
            className="mb-4"
        ) for option in document_options
    ]

    layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Documentos", className="mb-4"),
                dbc.Row(document_cards),
                dbc.Button("Volver", href="/dashboard/my-account/", color="primary", className="mt-3"),
            ], md=10, lg=8, className="mx-auto")
        ], className="justify-content-center")
    ], fluid=True, className="py-4")

    return layout