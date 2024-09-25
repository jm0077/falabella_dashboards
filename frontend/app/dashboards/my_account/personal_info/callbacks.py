from dash.dependencies import Input, Output, State
from flask_login import current_user
from app.auth.models import User
import dash_bootstrap_components as dbc

def register_callbacks(app):
    @app.callback(
        [Output("nombre", "value"),
         Output("apellido", "value"),
         Output("email", "value")],
        [Input("url", "pathname")]
    )
    def load_user_data(pathname):
        if pathname == "/dashboard/my-account/personal-info/" and current_user.is_authenticated:
            user = User.get(current_user.id)
            return user.first_name, user.last_name, user.email
        return "", "", ""

    @app.callback(
        Output("mensaje-resultado", "children"),
        [Input("guardar-datos", "n_clicks")],
        [State("nombre", "value"),
         State("apellido", "value"),
         State("email", "value")]
    )
    def update_user_data(n_clicks, nombre, apellido, email):
        if n_clicks and current_user.is_authenticated:
            user = User.get(current_user.id)
            try:
                user.update(first_name=nombre, last_name=apellido, email=email)
                return dbc.Alert("Datos actualizados correctamente", color="success")
            except Exception as e:
                return dbc.Alert(f"Error al actualizar los datos: {str(e)}", color="danger")
        return ""