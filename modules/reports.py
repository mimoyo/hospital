from flask import Blueprint, render_template
from models import db, Patient, Prescription, MedicalRecord, Appointment, Doctor
from sqlalchemy import func

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports/patient_prescriptions')
def report_patient_prescriptions():
    results = db.session.query(
        Patient.full_name,
        func.count(Prescription.id),
        func.coalesce(func.sum(Prescription.total_price), 0)
    ).join(MedicalRecord, MedicalRecord.patient_id == Patient.id) \
     .join(Prescription, Prescription.history_id == MedicalRecord.id) \
     .group_by(Patient.full_name).all()

    return render_template('reports/patient_prescriptions/report_patient_prescriptions.html', data=results)

@reports_bp.route('/reports/doctor_appointments')
def report_doctor_appointments():
    results = db.session.query(
        Doctor.full_name,
        func.count(Appointment.id)
    ).join(Appointment).group_by(Doctor.full_name).all()

    return render_template('reports/doctor_appointments/report_doctor_appointments.html', data=results)
