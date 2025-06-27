from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Department


departments_bp = Blueprint('departments', __name__)


# ========== Отделения ==========
@departments_bp.route('/departments')
def list_departments():
    departments = Department.query.all()
    return render_template('departments/list.html', departments=departments)

# ========== Добавить отделение ==========
@departments_bp.route('/departments/new', methods=['GET', 'POST'])
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
        return redirect(url_for('departments.list_departments'))
    return render_template('departments/form.html', department=None)

# ========== Изменить отделение ==========
@departments_bp.route('/departments/<int:department_id>/edit', methods=['GET', 'POST'])
def edit_department(department_id):
    department = Department.query.get_or_404(department_id)
    if request.method == 'POST':
        department.name = request.form['name']
        department.floor = request.form['floor']
        department.phone = request.form['phone']
        db.session.commit()
        flash('Отделение обновлено')
        return redirect(url_for('departments.list_departments'))
    return render_template('departments/form.html', department=department)

# ========== Удалить отделение ==========
@departments_bp.route('/departments/<int:department_id>/delete')
def delete_department(department_id):
    department = Department.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()
    flash('Отделение удалено')
    return redirect(url_for('departments.list_departments'))