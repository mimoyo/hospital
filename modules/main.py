from flask import Blueprint, render_template
from models import db, Patient, Appointment, Service

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    total_patients = db.session.query(Patient).count()
    total_appointments = db.session.query(Appointment).count()
    total_services = db.session.query(Service).count()

    return render_template('dashboard/main.html',
                           total_patients=total_patients,
                           total_appointments=total_appointments,
                           total_services=total_services)