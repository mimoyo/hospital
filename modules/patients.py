from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from models import db, Patient


patients_bp = Blueprint('patients', __name__)

# ========== Главная страница ==========
@patients_bp.route('/')
def index():
    return redirect(url_for('patients.list_patients'))


# ========== Список пациентов ==========
@patients_bp.route('/patients')
def list_patients():
    patients = Patient.query.all()
    return render_template('patients/list.html', patients=patients)


# ========== Добавить пациента ==========
@patients_bp.route('/patients/new', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        birth_date_str = request.form['birth_date']
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None

        new_patient = Patient(
            full_name=request.form['full_name'],
            birth_date=birth_date,
            gender=request.form['gender'],
            phone=request.form['phone'],
        )
        db.session.add(new_patient)
        db.session.commit()
        flash('Пациент добавлен успешно!')
        return redirect(url_for('patients.list_patients'))
    return render_template('patients/form.html', patient=None)


# ========== Редактировать пациента ==========
@patients_bp.route('/patients/<int:patient_id>/edit', methods=['GET', 'POST'])
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        patient.full_name = request.form['full_name']
        birth_date_str = request.form['birth_date']
        patient.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
        patient.gender = request.form['gender']
        patient.phone = request.form['phone']
        db.session.commit()
        flash('Пациент обновлён')
        return redirect(url_for('patients.list_patients'))
    return render_template('patients/form.html', patient=patient)


# ========== Удалить пациента ==========
@patients_bp.route('/patients/<int:patient_id>/delete')
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash('Пациент удалён')
    return redirect(url_for('patients.list_patients'))