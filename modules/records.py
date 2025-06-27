from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, MedicalRecord, Patient, Diagnosis
from datetime import datetime

records_bp = Blueprint('records', __name__)

@records_bp.route('/records')
def list_records():
    records = MedicalRecord.query.all()
    return render_template('records/list.html', records=records)

@records_bp.route('/records/new', methods=['GET', 'POST'])
def add_record():
    patients = Patient.query.all()
    diagnoses = Diagnosis.query.all()
    if request.method == 'POST':
        record = MedicalRecord(
            patient_id=int(request.form['patient_id']),
            diagnosis_id=int(request.form['diagnosis_id']),
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            notes=request.form['notes']
        )
        db.session.add(record)
        db.session.commit()
        flash('Запись добавлена')
        return redirect(url_for('records.list_records'))
    return render_template('records/form.html', record=None, patients=patients, diagnoses=diagnoses)

@records_bp.route('/records/<int:record_id>/edit', methods=['GET', 'POST'])
def edit_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    patients = Patient.query.all()
    diagnoses = Diagnosis.query.all()
    if request.method == 'POST':
        record.patient_id = int(request.form['patient_id'])
        record.diagnosis_id = int(request.form['diagnosis_id'])
        record.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        record.notes = request.form['notes']
        db.session.commit()
        flash('Запись обновлена')
        return redirect(url_for('records.list_records'))
    return render_template('records/form.html', record=record, patients=patients, diagnoses=diagnoses)

@records_bp.route('/records/<int:record_id>/delete')
def delete_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    flash('Запись удалена')
    return redirect(url_for('records.list_records'))