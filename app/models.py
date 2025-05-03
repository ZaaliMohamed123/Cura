from app import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    
    __table_args__ = (db.CheckConstraint("role IN ('Patient', 'Mentor')", name='role_check'),)

    mentorships_as_patient = db.relationship('Mentorship',foreign_keys='Mentorship.patient_id',back_populates='patient',cascade='all, delete-orphan')
    mentorships_as_mentor = db.relationship('Mentorship',foreign_keys='Mentorship.mentor_id',back_populates='mentor',cascade='all, delete-orphan')
    medications = db.relationship('Medications',back_populates='patient',cascade='all, delete-orphan')
    pharmacy = db.relationship('Pharmacies',back_populates='patient',uselist=False)
    appointments = db.relationship('Appointments',back_populates='patient',cascade='all, delete-orphan')
    pathologies = db.relationship('Pathologies',back_populates='patient',cascade='all, delete-orphan')
    adverse_reports = db.relationship('AI_Adverse_Effect_Reports',back_populates='patient',cascade='all, delete-orphan')
    medication_reminders = db.relationship('Medication_Reminders',back_populates='patient',cascade='all, delete-orphan')
    medication_logs = db.relationship('Medication_Intake_Logging',back_populates='patient',cascade='all, delete-orphan')

class Mentorship(db.Model):
    __tablename__ = 'mentorship'
    mentorship_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    relationship = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    
    patient = db.relationship('Users',foreign_keys=[patient_id],back_populates='mentorships_as_patient')
    mentor = db.relationship('Users',foreign_keys=[mentor_id],back_populates='mentorships_as_mentor')

class Medications(db.Model):
    __tablename__ = 'medications'
    medication_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    dosage = db.Column(db.String(50))
    frequency = db.Column(db.String(50))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)

    patient = db.relationship('Users',back_populates='medications')
    reminders = db.relationship('Medication_Reminders',back_populates='medication',cascade='all, delete-orphan')
    logs = db.relationship('Medication_Intake_Logging',back_populates='medication',cascade='all, delete-orphan')

class Medication_Reminders(db.Model):
    __tablename__ = 'medication_reminders'
    reminder_id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.medication_id', ondelete='CASCADE'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    reminder_time = db.Column(db.Time, nullable=False)

    medication = db.relationship('Medications',back_populates='reminders')
    patient = db.relationship('Users',back_populates='medication_reminders')

class Medication_Intake_Logging(db.Model):
    __tablename__ = 'medication_intake_logging'
    log_id = db.Column(db.Integer, primary_key=True)
    medication_id = db.Column(db.Integer, db.ForeignKey('medications.medication_id', ondelete='CASCADE'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    intake_time = db.Column(db.DateTime, nullable=False)
    dosage_taken = db.Column(db.String(50))
    effects = db.Column(db.Text)

    medication = db.relationship('Medications',back_populates='logs')
    patient = db.relationship('Users',back_populates='medication_logs')

class AI_Adverse_Effect_Reports(db.Model):
    __tablename__ = 'ai_adverse_effect_reports'
    report_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    risk_level = db.Column(db.String(50))
    details = db.Column(db.Text)
    generated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    patient = db.relationship('Users',back_populates='adverse_reports')

class Pathologies(db.Model):
    __tablename__ = 'pathologies'
    pathology_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    condition_name = db.Column(db.String(255), nullable=False)
    diagnosis_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    patient = db.relationship('Users',back_populates='pathologies')

class Pharmacies(db.Model):
    __tablename__ = 'pharmacies'
    pharmacy_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(255))

    patient = db.relationship('Users',back_populates='pharmacy')

class Appointments(db.Model):
    __tablename__ = 'appointments'
    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    doctor_name = db.Column(db.String(255), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    notes = db.Column(db.Text)

    patient = db.relationship('Users',back_populates='appointments')