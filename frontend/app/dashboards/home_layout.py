# app/dashboards/home_layout.py
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_home_layout():
    """
    Crea el layout inicial de la página principal.
    El contenido real será actualizado por los callbacks.
    """
    return html.Div([
        dcc.Store(id='user-status-store'),
        dcc.Store(id='user-status-updated'),
        html.Div(id='home-content')
    ])

def create_error_layout():
    return dbc.Container([
        html.H1("Error temporal", className="text-center mb-4"),
        html.P("Lo sentimos, estamos experimentando problemas técnicos. Por favor, intente más tarde.",
               className="text-center")
    ], className="mt-5", fluid="md")

def create_first_time_layout():
    return dbc.Container([
        html.H1("¡Bienvenido a tu Centro Financiero!", className="text-center mb-4"),
        html.P("Para poder ver la información de tus estados de cuenta, por favor carga tus documentos primero.",
               className="text-center"),
        dbc.Row([
            dbc.Col([
                dbc.Button("Cargar Documentos", href="/dashboard/my-account/documents/upload/",
                         color="primary", className="w-100")
            ], md=6, className="mx-auto")
        ], className="justify-content-center")
    ], className="mt-5", fluid="md")

def create_no_documents_layout():
    return dbc.Container([
        html.H1("Bienvenido de vuelta a tu Centro Financiero", className="text-center mb-4"),
        html.P("Para poder ver la información de tus estados de cuenta, por favor carga tus documentos primero.",
               className="text-center"),
        dbc.Row([
            dbc.Col([
                dbc.Button("Cargar Documentos", href="/dashboard/my-account/documents/upload/",
                         color="primary", className="w-100")
            ], md=6, className="mx-auto")
        ], className="justify-content-center")
    ], className="mt-5", fluid="md")

def create_default_layout():
    return dbc.Container([
        html.H1("Bienvenido de vuelta a tu Centro Financiero", className="text-center mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Img(src="https://www.bancofalabella.pe/assets/logo.svg",
                                   className="img-fluid mb-3",
                                   style={'max-height': '60px'}),
                        ], style={'height': '100px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                        dbc.Button("Ir a Falabella", href="/dashboard/falabella/",
                                 color="primary", className="w-100")
                    ])
                ], className="h-100")
            ], md=6, className="mb-3 mb-md-0"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Img(src="https://cdn.aglty.io/scotiabank-peru/Global-Rebrand/logo.svg",
                                   className="img-fluid mb-3",
                                   style={'max-height': '60px'}),
                        ], style={'height': '100px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                        dbc.Button("Ir a Scotiabank", href="/dashboard/scotiabank/",
                                 color="danger", className="w-100")
                    ])
                ], className="h-100")
            ], md=6)
        ], className="justify-content-center")
    ], className="mt-5", fluid="md")