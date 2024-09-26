from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from flask_login import current_user
from app.auth.models import User

def create_security_layout():
    layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Cambiar contraseña", className="mb-4"),
                dbc.Form([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Contraseña actual", html_for="contrasena-actual"),
                            dbc.Input(type="password", id="contrasena-actual", placeholder="Ingresa tu contraseña actual"),
                        ], width=12),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Nueva contraseña", html_for="nueva-contrasena"),
                            dbc.Input(type="password", id="nueva-contrasena", placeholder="Ingresa tu nueva contraseña"),
                        ], width=12),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Confirmar nueva contraseña", html_for="confirmar-contrasena"),
                            dbc.Input(type="password", id="confirmar-contrasena", placeholder="Confirma tu nueva contraseña"),
                        ], width=12),
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Guardar cambios", color="primary", id="guardar-contrasena", className="me-2"),
                            dbc.Button("Volver", href="/dashboard/my-account/", color="secondary", id="volver-seguridad"),
                        ], width=12),
                    ], className="mt-3"),
                ]),
                html.Div(id="mensaje-resultado-contrasena", className="mt-3")
            ], md=8, lg=6, className="mx-auto")
        ])
    ], fluid=True, className="py-4")

    return layout

def register_callbacks(app):
    @app.callback(
        Output("mensaje-resultado-contrasena", "children"),
        [Input("guardar-contrasena", "n_clicks")],
        [State("contrasena-actual", "value"),
         State("nueva-contrasena", "value"),
         State("confirmar-contrasena", "value")]
    )
    def update_password(n_clicks, contrasena_actual, nueva_contrasena, confirmar_contrasena):
        if n_clicks and current_user.is_authenticated:
            if nueva_contrasena != confirmar_contrasena:
                return dbc.Alert("Las nuevas contraseñas no coinciden", color="danger", dismissable=True)
            success, message = current_user.update_password(contrasena_actual, nueva_contrasena)
            if success:
                return dbc.Alert(message, color="success", dismissable=True)
            else:
                return dbc.Alert(message, color="danger", dismissable=True)
        return ""