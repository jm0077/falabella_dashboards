from .layout import create_layout
from .callbacks import register_callbacks

def create_scotiabank_dashboard():
    return create_layout()

def register_scotiabank_callbacks(app):
    register_callbacks(app)