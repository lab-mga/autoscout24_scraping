# routes/__init__.py
from .scrap import scrap_bp

def register_routes(app):
    app.register_blueprint(scrap_bp)