from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Department, Doctor, Category


doctors_bp = Blueprint('doctors', __name__)

# ===== Врачи =====
@doctors_bp.route('/doctors')
def list_doctors():
    doctors = Doctor.query.all()
    return render_template('doctors/list.html', doctors=doctors)


# ===== Добавить врача =====
@doctors_bp.route('/doctors/new', methods=['GET', 'POST'])
def add_doctor():
    departments = Department.query.all()
    categories = Category.query.all()
    if request.method == 'POST':
        department_id = request.form['department_id']
        doctor = Doctor(
            last_name = request.form['last_name'],
            first_name = request.form['first_name'],
            middle_name = request.form['middle_name'],
            specialty=request.form['specialty'],
            experience_years=request.form['experience_years'],
            phone=request.form['phone'],
            category_id=int(request.form['category_id']) if request.form['category_id'] else None,
            department_id=int(department_id) if department_id else None
        )
        db.session.add(doctor)
        db.session.commit()
        flash('Врач добавлен!')
        return redirect(url_for('doctors.list_doctors'))
    return render_template('doctors/form.html', doctor=None, departments=departments, categories=categories)

# ===== Изменить врача =====
@doctors_bp.route('/doctors/<int:doctor_id>/edit', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    departments = Department.query.all()
    categories = Category.query.all()
    if request.method == 'POST':
        doctor.last_name = request.form['last_name']
        doctor.first_name = request.form['first_name']
        doctor.middle_name = request.form['middle_name']
        doctor.specialty = request.form['specialty']
        doctor.experience_years = request.form['experience_years']
        doctor.phone = request.form['phone']
        department_id = request.form['department_id']
        category_id = request.form['category_id']
        doctor.department_id = int(department_id) if department_id else None
        doctor.category_id = int(category_id) if category_id else None
        db.session.commit()
        flash('Информация о враче обновлена!')
        return redirect(url_for('doctors.list_doctors'))
    return render_template('doctors/form.html', doctor=doctor, departments=departments, categories=categories)

# ===== Удалить врача =====
@doctors_bp.route('/doctors/<int:doctor_id>/delete')
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Врач удалён!')
    return redirect(url_for('doctors.list_doctors'))