from dash import html
import dash_bootstrap_components as dbc

def create_notifications_layout():
    layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Configuración de Notificaciones", className="mb-4"),
                html.P("Aquí puedes configurar tus preferencias de notificaciones."),
                # Aquí puedes agregar más elementos según sea necesario
                dbc.Button("Volver", href="/dashboard/my-account/configuration/", color="primary", className="mt-3"),
            ], md=10, lg=8, className="mx-auto")
        ], className="justify-content-center")
    ], fluid=True, className="py-4")

    return layout