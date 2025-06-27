from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Service

services_bp = Blueprint('services', __name__)

@services_bp.route('/services')
def list_services():
    services = Service.query.all()
    return render_template('services/list.html', services=services)

@services_bp.route('/services/new', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        service = Service(
            name=request.form['name'],
            price=request.form['price'],
            duration_min=request.form['duration_min']
        )
        db.session.add(service)
        db.session.commit()
        flash('Услуга добавлена')
        return redirect(url_for('services.list_services'))
    return render_template('services/form.html', service=None)

@services_bp.route('/services/<int:service_id>/edit', methods=['GET', 'POST'])
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    if request.method == 'POST':
        service.name = request.form['name']
        service.price = request.form['price']
        service.duration_min = request.form['duration_min']
        db.session.commit()
        flash('Услуга обновлена')
        return redirect(url_for('services.list_services'))
    return render_template('services/form.html', service=service)

@services_bp.route('/services/<int:service_id>/delete')
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash('Услуга удалена')
    return redirect(url_for('services.list_services'))
