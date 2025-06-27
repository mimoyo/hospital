from .doctors import doctors_bp
from .patients import patients_bp
from .appointments import appointments_bp
from .departments import departments_bp
from .diagnosis import diagnosis_bp
from .records import records_bp
from .services import services_bp
from .prescriptions import prescriptions_bp
from .reports import reports_bp


def register_blueprints(app):
    app.register_blueprint(doctors_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(departments_bp)
    app.register_blueprint(diagnosis_bp)
    app.register_blueprint(records_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(prescriptions_bp)
    app.register_blueprint(reports_bp)