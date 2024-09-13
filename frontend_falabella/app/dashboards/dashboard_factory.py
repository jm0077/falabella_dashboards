from dash import html, dcc
from dash.dependencies import Input, Output
from flask_login import login_required
from flask import redirect, url_for
from .falabella import create_falabella_dashboard
from .scotiabank import create_scotiabank_dashboard

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

    # Variables para controlar si los callbacks ya fueron registrados
    app.falabella_callbacks_registered = False
    app.scotiabank_callbacks_registered = False

    # Callback para cambiar el layout según la URL
    @app.callback(Output('page-content', 'children'),
                  Input('url', 'pathname'))
    def display_page(pathname):
        if not hasattr(display_page, 'login_required'):
            display_page.login_required = login_required(display_page)
            return display_page.login_required()
        
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

    # Ruta para manejar el acceso no autorizado
    @app.server.errorhandler(401)
    def unauthorized(error):
        return redirect(url_for('auth.login'))