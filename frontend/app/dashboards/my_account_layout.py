from dash import html
import dash_bootstrap_components as dbc

def create_my_account_layout():
    account_options = [
        {"title": "Datos personales", "description": "Edita tu nombre, avatar, correo electrónico y número de teléfono", "icon": "datos-personales.svg"},
        {"title": "Configuración", "description": "Edita tus límites de operación, configura tus tarjetas y notificaciones", "icon": "configuracion.svg"},
        {"title": "Seguridad", "description": "Configura tu Clave Digital y cambia tu contraseña", "icon": "seguridad.svg"},
        {"title": "Documentos", "description": "Estados de Cuenta, boletas de pago, notas y otros documentos", "icon": "documentos.svg"},
        {"title": "Centro de ayuda", "description": "Preguntas frecuentes, haz una consulta o déjanos un comentario", "icon": "centro-ayuda.svg"}
    ]

    account_cards = [
        dbc.Card(
            [
                dbc.CardBody([
                    html.Div([
                        html.Img(src=f"/static/img/my-account/{option['icon']}", className="account-icon me-3"),
                        html.Div([
                            html.H5(option['title'], className="card-title mb-1"),
                            html.P(option['description'], className="card-text"),
                        ], className="flex-grow-1"),
                        html.I(className="bi bi-chevron-right")
                    ], className="d-flex align-items-center")
                ])
            ],
            className="mb-4 account-card",
        ) for option in account_options
    ]

    layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Mi Cuenta", className="mb-4"),
                dbc.Row([
                    dbc.Col(account_cards[0], md=6, className="mb-4"),
                    dbc.Col(account_cards[1], md=6, className="mb-4"),
                ]),
                dbc.Row([
                    dbc.Col(account_cards[2], md=6, className="mb-4"),
                    dbc.Col(account_cards[3], md=6, className="mb-4"),
                ]),
                dbc.Row([
                    dbc.Col(account_cards[4], md=6, className="mb-4"),
                ]),
                dbc.Button("Volver", href="/dashboard/", color="primary", className="mt-3"),
            ], md=10, lg=8, className="mx-auto")
        ], className="justify-content-center")
    ], fluid=True, className="py-4")

    return layout