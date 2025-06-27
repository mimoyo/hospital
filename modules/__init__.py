from .doctors import doctors_bp

def register_blueprints(app):
    app.register_blueprint(doctors_bp)