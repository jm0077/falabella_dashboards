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
    
def create_no_banks_layout():
    return dbc.Container([
        html.H1("Bienvenido de vuelta a tu Centro Financiero", className="text-center mb-4"),
        html.P("Actualmente no hay información disponible para mostrar", className="text-center mb-3"),
        dbc.Row([
            dbc.Col([
                html.P([
                    "Si no has cargado documento aún, ",
                    html.A("ve a la sección de documentos", href="/dashboard/my-account/documents/", className="text-primary"),
                    " y carga tus estados de cuenta."
                ], className="text-center mb-3"),
                dbc.Button("Ir a Documentos", href="/dashboard/my-account/documents/", 
                           color="primary", className="w-100 mb-3")
            ], md=8, className="mx-auto")
        ], className="justify-content-center"),
        dbc.Row([
            dbc.Col([
                html.P([
                    "Si has deshabilitado el panel de tus tarjetas, ",
                    html.A("ve a la sección de configuración", href="/dashboard/my-account/configuration/cards/", className="text-primary"),
                    " y habilita las que desees visualizar."
                ], className="text-center mb-3"),
                dbc.Button("Ir a Configuración de Tarjetas", href="/dashboard/my-account/configuration/cards/", 
                           color="secondary", className="w-100")
            ], md=8, className="mx-auto")
        ], className="justify-content-center")
    ], className="mt-5", fluid="md")

def create_default_layout(user_banks):
    """
    Crea un layout predeterminado que muestra solo las tarjetas de bancos habilitados
    
    Args:
        user_banks (list): Lista de bancos del usuario con su estado de habilitación
    """
    # Mapa de configuraciones de bancos
    bank_configs = {
        'falabella': {
            'logo': "https://www.bancofalabella.pe/assets/logo.svg",
            'href': "/dashboard/falabella/",
            'color': "primary"
        },
        'scotiabank': {
            'logo': "https://cdn.aglty.io/scotiabank-peru/Global-Rebrand/logo.svg", 
            'href': "/dashboard/scotiabank/",
            'color': "danger"
        }
    }

    # Filtrar bancos habilitados
    enabled_banks = [
        bank for bank in user_banks
        if bank.get('habilitado', True) and bank.get('banco_nombre', '').lower() in bank_configs
    ]

    # Crear columnas para bancos habilitados
    bank_cols = []
    for bank in enabled_banks:
        bank_name = bank.get('banco_nombre', '').lower()
        config = bank_configs[bank_name]
        
        bank_col = dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Img(src=config['logo'],
                               className="img-fluid mb-3",
                               style={'max-height': '60px'}),
                    ], style={'height': '100px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                    dbc.Button(f"Ir a {bank.get('banco_nombre', 'Banco')}", href=config['href'],
                             color=config['color'], className="w-100")
                ])
            ], className="h-100")
        ], md=6, className="mb-3 mb-md-0")
        
        bank_cols.append(bank_col)

    # Si no hay bancos habilitados, mostrar mensaje
    if not bank_cols:
        return create_no_banks_layout()

    return dbc.Container([
        html.H1("Bienvenido de vuelta a tu Centro Financiero", className="text-center mb-4"),
        dbc.Row(bank_cols, className="justify-content-center")
    ], className="mt-5", fluid="md")