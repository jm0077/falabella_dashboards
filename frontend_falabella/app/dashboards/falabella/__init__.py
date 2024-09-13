from .layout import create_layout
from .callbacks import register_callbacks

def create_falabella_dashboard():
    return create_layout()

def register_falabella_callbacks(app):
    register_callbacks(app)