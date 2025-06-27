from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from models import db, Appointment, Doctor, Patient


appointments_bp = Blueprint('appointments', __name__)


# ===== Приёмы =====
@appointments_bp.route('/appointments')
def list_appointments():
    appointments = Appointment.query.all()
    return render_template('appointments/list.html', appointments=appointments)

# ========== Добавление приема ==========
@appointments_bp.route('/appointments/new', methods=['GET', 'POST'])
def add_appointment():
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    if request.method == 'POST':
        appointment_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date()
        appointment_time = datetime.strptime(request.form['appointment_time'], '%H:%M').time()
        new_appointment = Appointment(
            patient_id=request.form['patient_id'],
            doctor_id=request.form['doctor_id'],
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            room_number=request.form['room_number']
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash('Приём добавлен!')
        return redirect(url_for('appointments.list_appointments'))
    return render_template('appointments/form.html', patients=patients, doctors=doctors, appointment=None)

# ========== Изменение приема ==========
@appointments_bp.route('/appointments/<int:appointment_id>/edit', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    if request.method == 'POST':
        appointment.appointment_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%d').date()
        time_str = request.form['appointment_time'][:5]
        appointment.appointment_time = datetime.strptime(time_str, '%H:%M').time()
        appointment.patient_id = request.form['patient_id']
        appointment.doctor_id = request.form['doctor_id']
        appointment.room_number = request.form['room_number']
        db.session.commit()
        flash('Приём обновлён')
        return redirect(url_for('appointments.list_appointments'))
    return render_template('appointments/form.html', appointment=appointment, patients=patients, doctors=doctors)

# ========== Удаление приема ==========
@appointments_bp.route('/appointments/<int:appointment_id>/delete')
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Приём удалён')
    return redirect(url_for('appointments.list_appointments'))