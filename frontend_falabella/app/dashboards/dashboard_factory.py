from flask_login import login_required
from .falabella import create_falabella_dashboard
# Importa otros dashboards aquí

def create_dashboards(app):
    # Falabella Dashboard
    #falabella_layout, falabella_callbacks = create_falabella_dashboard(app)
    #app.layout = falabella_layout
    #falabella_callbacks(app)
    app.layout = create_falabella_dashboard(app)

    # Proteger todas las rutas del dashboard
    for view_function in app.server.view_functions:
        if view_function.startswith('/dashboard/'):
            app.server.view_functions[view_function] = login_required(app.server.view_functions[view_function])

    # Aquí puedes agregar más dashboards si es necesario