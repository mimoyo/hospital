from .doctors import doctors_bp
from .patients import patients_bp
from .appointments import appointments_bp
from .departments import departments_bp
from .diagnosis import diagnosis_bp

def register_blueprints(app):
    app.register_blueprint(doctors_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(departments_bp)
    app.register_blueprint(diagnosis_bp)