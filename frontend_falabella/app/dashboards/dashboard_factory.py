from dash import html, dcc
from dash.dependencies import Input, Output
from flask_login import login_required
from flask import redirect, url_for
from .falabella import create_falabella_dashboard, register_falabella_callbacks
from .scotiabank import create_scotiabank_dashboard, register_scotiabank_callbacks

def create_dashboards(app, oauth):
    def protect_dashviews(app):
        for view_func in app.server.view_functions:
            if view_func.startswith('/dashboard'):
                app.server.view_functions[view_func] = login_required(app.server.view_functions[view_func])

    # Proteger todas las vistas de Dash
    protect_dashviews(app)

    # Crear un layout principal para Dash
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])

    register_falabella_callbacks(app)
    register_scotiabank_callbacks(app)

    # Callback para cambiar el layout según la URL
    @app.callback(Output('page-content', 'children'),
                  Input('url', 'pathname'))
    @login_required
    def display_page(pathname):
        if pathname == '/dashboard/falabella/':
            return create_falabella_dashboard()
        elif pathname == '/dashboard/scotiabank/':
            return create_scotiabank_dashboard()
        else:
            return html.Div('404: Not Found')  # Página no encontrada

    # Ruta para manejar el acceso no autorizado
    @app.server.errorhandler(401)
    def unauthorized(error):
        return redirect(url_for('auth.login'))