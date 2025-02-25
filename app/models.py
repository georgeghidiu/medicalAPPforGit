    # Din biblioteca datetime importam datetime pentru data si ora corecta a programarilor
from datetime import datetime

    # # flask-login oferă funcționalități de autentificare, iar `UserMixin` facilitează gestionarea utilizatorilor
from flask_login import UserMixin

    # hash-uirea și verificarea parolelor
from werkzeug.security import check_password_hash, generate_password_hash

    # din app/database.py importam obiectul db pentru definirea modelelor bazei de date
from app.database import db

    #   defineste modelul user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hash-ul parolei
    role = db.Column(db.String(10), nullable=False)  # pentru a sti daca este "doctor" sau "pacient"

    # transforma parola primita in parola securizata
    def set_password(self, password):
        """Setează parola utilizatorului (hash-uită)."""
        self.password = generate_password_hash(password)

    # verifica daca parola se potriveste cu hash-ul
    def check_password(self, password):
        """Verifică parola introdusă cu hash-ul salvat."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'

    # defineste modelul doctor in baza de date
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    specialization = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)  # Ani de experiență

    user = db.relationship('User', backref=db.backref('doctor_profile', uselist=False))

    def __repr__(self):
        return f'<Doctor {self.user.username} - {self.specialization}>' if self.user else '<Doctor without user>'

    # defineste modelul programari in baza de date
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default="pending")  # pending, confirmed, canceled sau altele pe care le voi face mai tarziu

    patient = db.relationship('User', backref=db.backref('appointments', lazy=True))
    doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy=True))

    def __repr__(self):
        doctor_name = self.doctor.user.username if self.doctor and self.doctor.user else "Unknown Doctor"
        patient_name = self.patient.username if self.patient else "Unknown Patient"
        return f'<Appointment {patient_name} with {doctor_name} on {self.date}>'
