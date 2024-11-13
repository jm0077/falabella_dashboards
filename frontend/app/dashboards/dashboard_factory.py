from dash import html, dcc, no_update
from dash.dependencies import Input, Output, State
from flask_login import login_required, logout_user, current_user
from flask import redirect, url_for, session
from .falabella import create_falabella_dashboard, register_falabella_callbacks
from .scotiabank import create_scotiabank_dashboard, register_scotiabank_callbacks
from .navbar import create_navbar
from .home_layout import create_home_layout
from .home_callbacks import register_home_callbacks
from .my_account import create_my_account_layout
from .my_account.personal_info import create_personal_info_layout, register_callbacks as register_personal_info_callbacks
from .my_account.security.layout import create_security_layout, register_callbacks as register_security_callbacks
from .my_account.help_center.layout import create_help_center_layout
from .my_account.configuration.layout import create_configuration_layout
from .my_account.configuration.cards.layout import create_cards_layout
from .my_account.configuration.cards.callbacks import register_callbacks as register_cards_callbacks
from .my_account.configuration.notifications.layout import create_notifications_layout
from .my_account.documents.layout import create_documents_layout
from .my_account.documents.callbacks import register_callbacks as register_documents_callbacks
from .my_account.documents.upload.layout import create_upload_documents_layout
from .my_account.documents.upload.callbacks import register_upload_callbacks

def create_dashboards(app):
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

    register_home_callbacks(app)
    register_falabella_callbacks(app)
    register_scotiabank_callbacks(app)
    register_personal_info_callbacks(app)
    register_security_callbacks(app)
    register_cards_callbacks(app)
    register_documents_callbacks(app)
    register_upload_callbacks(app)

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
        elif pathname == '/dashboard/my-account/':
            return create_my_account_layout()
        elif pathname == '/dashboard/my-account/personal-info/':
            return create_personal_info_layout()
        elif pathname == '/dashboard/my-account/security/':
            return create_security_layout()
        elif pathname == '/dashboard/my-account/help-center/':
            return create_help_center_layout()
        elif pathname == '/dashboard/my-account/configuration/':
            return create_configuration_layout()
        elif pathname == '/dashboard/my-account/configuration/cards/':
            return create_cards_layout()
        elif pathname == '/dashboard/my-account/configuration/notifications/':
            return create_notifications_layout()
        elif pathname == '/dashboard/my-account/documents/':
            return create_documents_layout()
        elif pathname == '/dashboard/my-account/documents/upload/':
            return create_upload_documents_layout()
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