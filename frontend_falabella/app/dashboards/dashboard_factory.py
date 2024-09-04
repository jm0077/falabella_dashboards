from flask_login import login_required
from dash import html, dcc
from dash.dependencies import Input, Output
from .falabella import create_falabella_dashboard
from .scotiabank import create_scotiabank_dashboard

def create_dashboards(app):
    # Falabella Dashboard
    falabella_layout = create_falabella_dashboard(app)

    # Scotiabank Dashboard
    scotiabank_layout = create_scotiabank_dashboard(app)

    # Proteger todas las rutas del dashboard
    for view_function in app.server.view_functions:
        if view_function.startswith('/dashboard/'):
            app.server.view_functions[view_function] = login_required(app.server.view_functions[view_function])

    # Crear un layout principal que incluye un contenedor donde cambiará el layout
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')  # Contenedor que cambiará de contenido
    ])

    # Callback para cambiar el layout según la URL
    @app.callback(Output('page-content', 'children'),
                  Input('url', 'pathname'))
    def display_page(pathname):
        if pathname == '/dashboard/falabella/':
            return falabella_layout
        elif pathname == '/dashboard/scotiabank/':
            return scotiabank_layout
        else:
            return html.Div('404: Not Found')  # Página no encontrada
