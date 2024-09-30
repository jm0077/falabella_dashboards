from dash import Input, Output, State, callback_context, ALL, html, MATCH
from dash.exceptions import PreventUpdate
import requests
from flask import current_app
from flask_login import current_user
import json
import dash_bootstrap_components as dbc
from config import CARDS_API_ENDPOINT

def register_callbacks(app):
    @app.callback(
        Output("cards-container", "children"),
        Input("url", "pathname")
    )
    def load_cards(pathname):
        if pathname != "/dashboard/my-account/configuration/cards/":
            raise PreventUpdate

        user_id = current_user.id
        api_url = f"{CARDS_API_ENDPOINT}/usuario-bancos?userId={user_id}"

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            user_banks = response.json()

            from .layout import create_card_component

            cards = []
            for bank in user_banks:
                bank_id = bank['banco_id']
                bank_logo = f"/static/img/{bank['banco_nombre'].lower().replace(' ', '_')}_logo.svg"
                enabled = bank['habilitado']
                cards.append(create_card_component(bank_id, bank_logo, enabled))

            return cards

        except requests.RequestException as e:
            return html.Div(f"Error al cargar las tarjetas: {str(e)}", className="text-danger")

    @app.callback(
        Output({"type": "bank-switch", "index": MATCH}, "value"),
        Output({"type": "flash-message", "index": MATCH}, "children"),
        Input({"type": "bank-switch", "index": MATCH}, "value"),
        State({"type": "bank-switch", "index": MATCH}, "id"),
        State("url", "pathname"),
        prevent_initial_call=True
    )
    def update_card_status(value, id, pathname):
        ctx = callback_context
        if not ctx.triggered or pathname != "/dashboard/my-account/configuration/cards/":
            raise PreventUpdate

        bank_id = id['index']
        user_id = current_user.id
        api_url = f"{CARDS_API_ENDPOINT}/usuario-bancos"

        data = {
            "userId": user_id,
            "banco_id": bank_id,
            "habilitado": value
        }

        try:
            response = requests.put(api_url, json=data)
            response.raise_for_status()
            return value, dbc.Alert("Actualizado correctamente", color="success", dismissable=True, duration=4000)
        except requests.RequestException as e:
            # En caso de error, revertimos el switch a su estado anterior
            return not value, dbc.Alert(f"Error al actualizar el estado de la tarjeta: {str(e)}", color="danger", dismissable=True, duration=4000)