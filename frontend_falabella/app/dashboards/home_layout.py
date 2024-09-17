from dash import html
import dash_bootstrap_components as dbc

def create_home_layout():
    return dbc.Container([
        html.H1("Bienvenido a tu Centro Financiero", className="text-center mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Img(src="https://www.bancofalabella.pe/assets/logo.svg", className="img-fluid mb-3", style={'max-height': '60px'}),
                        ], style={'height': '100px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                        dbc.Button("Ir a Falabella", href="/dashboard/falabella/", color="primary", className="w-100")
                    ])
                ], className="h-100")  # Make the card take full height
            ], md=6, className="mb-3 mb-md-0"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.Img(src="https://cdn.aglty.io/scotiabank-peru/Global-Rebrand/logo.svg", className="img-fluid mb-3", style={'max-height': '60px'}),
                        ], style={'height': '100px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                        dbc.Button("Ir a Scotiabank", href="/dashboard/scotiabank/", color="danger", className="w-100")
                    ])
                ], className="h-100")  # Make the card take full height
            ], md=6)
        ], className="justify-content-center")
    ], className="mt-5", fluid="md")