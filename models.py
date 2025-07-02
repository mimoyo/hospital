from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    floor = db.Column(db.Integer)
    phone = db.Column(db.String(20))

    doctors = db.relationship('Doctor', backref='department', lazy=True)


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    doctors = db.relationship('Doctor', backref='category', lazy=True)

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    insurance_number = db.Column(db.String(30))

    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy=True)


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    appointment_date = db.Column(db.Date)
    appointment_time = db.Column(db.Time)
    room_number = db.Column(db.String(10))

class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))
    name = db.Column(db.String(100))
    description = db.Column(db.Text)

    medical_records = db.relationship('MedicalRecord', backref='diagnosis', lazy=True)


class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnoses.id'))
    date = db.Column(db.Date)
    notes = db.Column(db.Text)

    prescriptions = db.relationship('Prescription', backref='medical_record', lazy=True)


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    duration_min = db.Column(db.Integer)

    prescriptions = db.relationship('Prescription', backref='service', lazy=True)


class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    id = db.Column(db.Integer, primary_key=True)
    history_id = db.Column(db.Integer, db.ForeignKey('medical_records.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Numeric(10, 2))