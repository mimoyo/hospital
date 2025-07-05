from flask import Blueprint, render_template, request
from models import db, Patient, Prescription, MedicalRecord, Appointment, Doctor, Diagnosis
from sqlalchemy import func

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports/patient_prescriptions')
def report_patient_prescriptions():
    results = db.session.query(
        Patient.last_name,
        Patient.first_name,
        Patient.middle_name,
        func.count(Prescription.id),
        func.coalesce(func.sum(Prescription.total_price), 0)
    ).join(MedicalRecord, MedicalRecord.patient_id == Patient.id) \
     .join(Prescription, Prescription.history_id == MedicalRecord.id) \
     .group_by(Patient.last_name, Patient.first_name, Patient.middle_name).all()

    return render_template('reports/patient_prescriptions/report_patient_prescriptions.html', data=results)

@reports_bp.route('/reports/doctor_appointments')
def report_doctor_appointments():
    results = db.session.query(
        Doctor.last_name,
        Doctor.first_name,
        Doctor.middle_name,
        func.count(Appointment.id)
    ).join(Appointment).group_by(Doctor.last_name, Doctor.first_name, Doctor.middle_name).all()

    return render_template('reports/doctor_appointments/report_doctor_appointments.html', data=results)

@reports_bp.route('/reports/diagnosis_by_period', methods=['GET', 'POST'])
def report_diagnosis_by_period():
    patients = Patient.query.all()
    results = []

    if request.method == 'POST':
        patient_id = request.form['patient_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        results = db.session.query(
            Diagnosis.name,
            Diagnosis.code,
            MedicalRecord.date,
            MedicalRecord.notes
        ).join(MedicalRecord.diagnosis
        ).filter(
            MedicalRecord.patient_id == patient_id,
            MedicalRecord.date.between(start_date, end_date)
        ).all()

    return render_template('reports/diagnosis_by_period/report_diagnosis_by_period.html', patients=patients, results=results)

