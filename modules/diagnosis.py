from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Diagnosis

diagnosis_bp = Blueprint('diagnosis', __name__)
@diagnosis_bp.route('/diagnosis')
def list_diagnosis():
    diagnoses = Diagnosis.query.all()
    return render_template('diagnosis/list.html', diagnoses=diagnoses)

@diagnosis_bp.route('/diagnosis/new', methods=['GET', 'POST'])
def add_diagnosis():
    if request.method == 'POST':
        diag = Diagnosis(
            code=request.form['code'],
            name=request.form['name'],
            description=request.form['description']
        )
        db.session.add(diag)
        db.session.commit()
        flash('Диагноз добавлен!')
        return redirect(url_for('diagnosis.list_diagnosis'))
    return render_template('diagnosis/form.html', diagnosis=None)

@diagnosis_bp.route('/diagnosis/<int:diagnosis_id>/edit', methods=['GET', 'POST'])
def edit_diagnosis(diagnosis_id):
    diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
    if request.method == 'POST':
        diagnosis.code = request.form['code']
        diagnosis.name = request.form['name']
        diagnosis.description = request.form['description']
        db.session.commit()
        flash('Диагноз обновлён')
        return redirect(url_for('diagnosis.list_diagnosis'))
    return render_template('diagnosis/form.html', diagnosis=diagnosis)

@diagnosis_bp.route('/diagnosis/<int:diagnosis_id>/delete')
def delete_diagnosis(diagnosis_id):
    diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
    db.session.delete(diagnosis)
    db.session.commit()
    flash('Диагноз удалён')
    return redirect(url_for('diagnosis.list_diagnoses'))
