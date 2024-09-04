from .layout import create_layout
from .callbacks import register_callbacks

def create_falabella_dashboard(app):
    if not hasattr(app, 'falabella_callbacks_registered') or not app.falabella_callbacks_registered:
        register_callbacks(app)
        app.falabella_callbacks_registered = True
    return create_layout()
