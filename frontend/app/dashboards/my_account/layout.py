from dash import html, dcc
import dash_bootstrap_components as dbc

def create_my_account_layout():
    account_options = [
        {"title": "Datos personales", "description": "Edita tu nombre, apellidos y correo electrónico", "icon": "datos-personales.svg", "href": "/dashboard/my-account/personal-info/"},
        {"title": "Configuración", "description": "Configura tus tarjetas y notificaciones", "icon": "configuracion.svg", "href": "#"},
        {"title": "Seguridad", "description": "Cambia tu contraseña", "icon": "seguridad.svg", "href": "#"},
        {"title": "Documentos", "description": "Estados de Cuenta y otros documentos", "icon": "documentos.svg", "href": "#"},
        {"title": "Centro de ayuda", "description": "Preguntas frecuentes, haz una consulta o déjanos un comentario", "icon": "centro-ayuda.svg", "href": "#"}
    ]

    account_cards = [
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
        ) for option in account_options
    ]

    layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Mi Cuenta", className="mb-4"),
                dbc.Row(account_cards),
                dbc.Button("Volver", href="/dashboard/", color="primary", className="mt-3"),
            ], md=10, lg=8, className="mx-auto")
        ], className="justify-content-center")
    ], fluid=True, className="py-4")

    return layout