from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from flask_login import current_user
from app.auth.models import User

def create_personal_info_layout():
    layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Datos Personales", className="mb-4"),
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("DNI", html_for="dni"),
                            dbc.Input(type="text", id="dni", placeholder="Ingresa tu número de documento"),
                        ], width=12),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Nombre", html_for="nombre"),
                            dbc.Input(type="text", id="nombre", placeholder="Ingresa tu nombre"),
                        ], width=12),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Apellido", html_for="apellido"),
                            dbc.Input(type="text", id="apellido", placeholder="Ingresa tu apellido"),
                        ], width=12),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Correo electrónico", html_for="email"),
                            dbc.Input(type="email", id="email", placeholder="Ingresa tu correo electrónico"),
                        ], width=12),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Guardar cambios", color="primary", id="guardar-datos", className="me-2"),
                            dbc.Button("Volver", href="/dashboard/my-account/", color="secondary", id="volver-datos"),
                        ], width=12),
                    ], className="mt-3"),
                ]),
                html.Div(id="mensaje-resultado", className="mt-3")
            ], md=8, lg=6, className="mx-auto")
        ])
    ], fluid=True, className="py-4")

    return layout

def register_callbacks(app):
    @app.callback(
        [Output("dni", "value"),
         Output("nombre", "value"),
         Output("apellido", "value"),
         Output("email", "value")],
        [Input("url", "pathname")]
    )
    def load_user_data(pathname):
        if pathname == "/dashboard/my-account/personal-info/" and current_user.is_authenticated:
            return current_user.dni, current_user.first_name, current_user.last_name, current_user.email
        return "", "", "", ""

    @app.callback(
        Output("mensaje-resultado", "children"),
        [Input("guardar-datos", "n_clicks")],
        [State("dni", "value"),
         State("nombre", "value"),
         State("apellido", "value"),
         State("email", "value")]
    )
    def update_user_data(n_clicks, dni, nombre, apellido, email):
        if n_clicks and current_user.is_authenticated:
            success, message = current_user.update(dni=dni, first_name=nombre, last_name=apellido, email=email)
            if success:
                return dbc.Alert(message, color="success", dismissable=True)
            else:
                return dbc.Alert(message, color="danger", dismissable=True)
        return ""