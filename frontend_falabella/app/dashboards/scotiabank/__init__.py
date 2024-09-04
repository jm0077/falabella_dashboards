from .layout import create_layout
from .callbacks import register_callbacks

def create_scotiabank_dashboard(app):
    if not hasattr(app, 'scotiabank_callbacks_registered') or not app.scotiabank_callbacks_registered:
        register_callbacks(app)
        app.scotiabank_callbacks_registered = True
    return create_layout()
