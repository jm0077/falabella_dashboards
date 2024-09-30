from dash import html, dcc
import dash_bootstrap_components as dbc

def create_cards_layout():
    layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Configuración de Tarjetas", className="mb-4"),
                html.P("Aquí puedes habilitar tus tarjetas para el panel de tu centro financiero", className="mb-4"),
                html.Div(id="cards-container"),
                dbc.Button("Volver", href="/dashboard/my-account/configuration/", color="primary", className="mt-3"),
            ], md=10, lg=8, className="mx-auto")
        ], className="justify-content-center"),
        dbc.Row([
            dbc.Col([
                html.Div(id="flash-message", className="mt-3"),
            ], md=10, lg=8, className="mx-auto")
        ], className="justify-content-center"),
        dcc.Loading(
            id="loading-cards",
            type="default",
            children=html.Div(id="loading-output-cards")
        ),
    ], fluid=True, className="py-4")

    return layout

def create_card_component(bank_id, bank_logo, enabled):
    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(html.Img(src=bank_logo, className="img-fluid bank-logo"), width=6),
                dbc.Col(
                    dbc.Switch(
                        id={"type": "bank-switch", "index": bank_id},
                        value=enabled,
                        className="float-end custom-switch"
                    ),
                    width=6,
                    className="d-flex align-items-center justify-content-end"
                ),
            ], align="center"),
        ]),
        className="mb-3"
    )