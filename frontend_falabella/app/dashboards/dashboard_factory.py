from flask_login import login_required
from dash import html, dcc
from dash.dependencies import Input, Output
from .falabella import create_falabella_dashboard
from .scotiabank import create_scotiabank_dashboard

def create_dashboards(app):
    # Proteger todas las rutas del dashboard
    for view_function in app.server.view_functions:
        if view_function.startswith('/dashboard/'):
            app.server.view_functions[view_function] = login_required(app.server.view_functions[view_function])

    # Crear un layout principal que incluye un contenedor donde cambiará el layout
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')  # Contenedor que cambiará de contenido
    ])

    # Variables para controlar si los callbacks ya fueron registrados
    app.falabella_callbacks_registered = False
    app.scotiabank_callbacks_registered = False

    # Callback para cambiar el layout según la URL
    @app.callback(Output('page-content', 'children'),
                  Input('url', 'pathname'))
    def display_page(pathname):
        if pathname == '/dashboard/falabella/':
            if not app.falabella_callbacks_registered:
                create_falabella_dashboard(app)
                app.falabella_callbacks_registered = True
            return create_falabella_dashboard(app)
        elif pathname == '/dashboard/scotiabank/':
            if not app.scotiabank_callbacks_registered:
                create_scotiabank_dashboard(app)
                app.scotiabank_callbacks_registered = True
            return create_scotiabank_dashboard(app)
        else:
            return html.Div('404: Not Found')  # Página no encontrada
