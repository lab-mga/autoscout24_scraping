# routes/__init__.py
from .scrap import scrap_bp
from .analyze import analyze_bp

def register_routes(app):
    app.register_blueprint(scrap_bp)
    app.register_blueprint(analyze_bp)