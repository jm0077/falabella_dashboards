from .layout import create_layout
from .callbacks import register_callbacks

def create_falabella_dashboard(app):
    layout = create_layout()
    #callbacks = lambda app: register_callbacks(app)
    # Registro de callbacks de manera directa
    register_callbacks(app)
    return layout