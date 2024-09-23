from dash import html, dcc, no_update
from dash.dependencies import Input, Output, State
from flask_login import login_required, logout_user, current_user
from flask import redirect, url_for, session
from .falabella import create_falabella_dashboard, register_falabella_callbacks
from .scotiabank import create_scotiabank_dashboard, register_scotiabank_callbacks
from .navbar import create_navbar
from .home_layout import create_home_layout

def create_dashboards(app, oauth):
    def protect_dashviews(app):
        for view_func in app.server.view_functions:
            if view_func.startswith('/dashboard'):
                app.server.view_functions[view_func] = login_required(app.server.view_functions[view_func])

    # Proteger todas las vistas de Dash
    protect_dashviews(app)

    # Crear un layout principal para Dash
    app.layout = html.Div([
        dcc.Location(id='url', refresh=True),
        html.Div(id='navbar-container'),
        html.Div(id='page-content')
    ])

    register_falabella_callbacks(app)
    register_scotiabank_callbacks(app)

    @app.callback(
        Output('navbar-container', 'children'),
        Input('url', 'pathname')
    )
    def update_navbar(pathname):
        return create_navbar()

    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname'),
        State('url', 'search')
    )
    def display_page(pathname, search):
        if not current_user.is_authenticated:
            return dcc.Location(pathname="/auth/login", id="redirect-to-login")
        
        if pathname == '/dashboard/falabella/':
            return create_falabella_dashboard()
        elif pathname == '/dashboard/scotiabank/':
            return create_scotiabank_dashboard()
        elif pathname == '/auth/logout':
            return dcc.Location(pathname="/auth/logout", id="redirect-to-logout")
        else:
            return create_home_layout()

    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    # Ruta para manejar el acceso no autorizado
    @app.server.errorhandler(401)
    def unauthorized(error):
        return redirect(url_for('auth.login'))

    return app