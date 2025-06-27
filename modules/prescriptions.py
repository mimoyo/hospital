from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Prescription, MedicalRecord, Service

prescriptions_bp = Blueprint('prescriptions', __name__)

@prescriptions_bp.route('/prescriptions')
def list_prescriptions():
    prescriptions = Prescription.query.all()
    return render_template('prescriptions/list.html', prescriptions=prescriptions)

@prescriptions_bp.route('/prescriptions/new', methods=['GET', 'POST'])
def add_prescription():
    records = MedicalRecord.query.all()
    services = Service.query.all()
    if request.method == 'POST':
        history_id = int(request.form['history_id'])
        service_id = int(request.form['service_id'])
        quantity = int(request.form['quantity'])

        service = Service.query.get(service_id)
        total_price = service.price * quantity

        prescription = Prescription(
            history_id=history_id,
            service_id=service_id,
            quantity=quantity,
            total_price=total_price
        )
        db.session.add(prescription)
        db.session.commit()
        flash('Назначение добавлено')
        return redirect(url_for('prescriptions.list_prescriptions'))
    return render_template('prescriptions/form.html', prescription=None, records=records, services=services)

@prescriptions_bp.route('/prescriptions/<int:prescription_id>/edit', methods=['GET', 'POST'])
def edit_prescription(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    records = MedicalRecord.query.all()
    services = Service.query.all()
    if request.method == 'POST':
        prescription.history_id = int(request.form['history_id'])
        prescription.service_id = int(request.form['service_id'])
        prescription.quantity = int(request.form['quantity'])

        service = Service.query.get(prescription.service_id)
        prescription.total_price = service.price * prescription.quantity

        db.session.commit()
        flash('Назначение обновлено')
        return redirect(url_for('prescriptions.list_prescriptions'))
    return render_template('prescriptions/form.html', prescription=prescription, records=records, services=services)

@prescriptions_bp.route('/prescriptions/<int:prescription_id>/delete')
def delete_prescription(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    db.session.delete(prescription)
    db.session.commit()
    flash('Назначение удалено')
    return redirect(url_for('prescriptions.list_prescriptions'))
