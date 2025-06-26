from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Appointment, Department, Doctor, Patient
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'  # нужен для flash()

db.init_app(app)

# Создание таблиц
with app.app_context():
    db.create_all()


# ========== Главная страница ==========
@app.route('/')
def index():
    return redirect(url_for('list_patients'))


# ========== Список пациентов ==========
@app.route('/patients')
def list_patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)


# ========== Добавить пациента ==========
@app.route('/patients/new', methods=['GET', 'POST'])
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
        return redirect(url_for('list_patients'))
    return render_template('patient_form.html', patient=None)


# ========== Редактировать пациента ==========
@app.route('/patients/<int:patient_id>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('list_patients'))
    return render_template('patient_form.html', patient=patient)


# ========== Удалить пациента ==========
@app.route('/patients/<int:patient_id>/delete')
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash('Пациент удалён')
    return redirect(url_for('list_patients'))


# ===== Врачи =====
@app.route('/doctors')
def list_doctors():
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)


# ===== Добавить врача =====
@app.route('/doctors/new', methods=['GET', 'POST'])
def add_doctor():
    departments = Department.query.all()
    if request.method == 'POST':
        department_id = request.form['department_id']
        doctor = Doctor(
            full_name=request.form['full_name'],
            specialty=request.form['specialty'],
            category=request.form['category'],
            experience_years=request.form['experience_years'],
            phone=request.form['phone'],
            department_id=int(department_id) if department_id else None
        )
        db.session.add(doctor)
        db.session.commit()
        flash('Врач добавлен!')
        return redirect(url_for('list_doctors'))
    return render_template('doctor_form.html', doctor=None, departments=departments)

# ===== Изменить врача =====
@app.route('/doctors/<int:doctor_id>/edit', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    departments = Department.query.all()
    if request.method == 'POST':
        doctor.full_name = request.form['full_name']
        doctor.specialty = request.form['specialty']
        doctor.category = request.form['category']
        doctor.experience_years = request.form['experience_years']
        doctor.phone = request.form['phone']
        department_id = request.form['department_id']
        doctor.department_id = int(department_id) if department_id else None
        db.session.commit()
        flash('Информация о враче обновлена!')
        return redirect(url_for('list_doctors'))
    return render_template('doctor_form.html', doctor=doctor, departments=departments)

# ===== Удалить врача =====
@app.route('/doctors/<int:doctor_id>/delete')
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Врач удалён!')
    return redirect(url_for('list_doctors'))

# ===== Приёмы =====
@app.route('/appointments')
def list_appointments():
    appointments = Appointment.query.all()
    return render_template('appointments.html', appointments=appointments)

# ========== Добавление приема ==========
@app.route('/appointments/new', methods=['GET', 'POST'])
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
        return redirect(url_for('list_appointments'))
    return render_template('appointment_form.html', patients=patients, doctors=doctors, appointment=None)

# ========== Изменение приема ==========
@app.route('/appointments/<int:appointment_id>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('list_appointments'))
    return render_template('appointment_form.html', appointment=appointment, patients=patients, doctors=doctors)

# ========== Удаление приема ==========
@app.route('/appointments/<int:appointment_id>/delete')
def delete_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Приём удалён')
    return redirect(url_for('list_appointments'))

# ========== Отделения ==========
@app.route('/departments')
def list_departments():
    departments = Department.query.all()
    return render_template('departments.html', departments=departments)

# ========== Добавить отделение ==========
@app.route('/departments/new', methods=['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        dep = Department(
            name=request.form['name'],
            floor=request.form['floor'],
            phone=request.form['phone']
        )
        db.session.add(dep)
        db.session.commit()
        flash('Отделение добавлено')
        return redirect(url_for('list_departments'))
    return render_template('department_form.html', department=None)

# ========== Изменить отделение ==========
@app.route('/departments/<int:department_id>/edit', methods=['GET', 'POST'])
def edit_department(department_id):
    department = Department.query.get_or_404(department_id)
    if request.method == 'POST':
        department.name = request.form['name']
        department.floor = request.form['floor']
        department.phone = request.form['phone']
        db.session.commit()
        flash('Отделение обновлено')
        return redirect(url_for('list_departments'))
    return render_template('department_form.html', department=department)

# ========== Удалить отделение ==========
@app.route('/departments/<int:department_id>/delete')
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()
    flash('Отделение удалено')
    return redirect(url_for('list_departments'))

# ========== Запуск сервера ==========
if __name__ == '__main__':
    app.run(debug=True)
