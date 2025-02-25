from datetime import datetime

from flask import render_template, Blueprint, url_for, flash, request, redirect #Importa functii din Flask

# Import pentru gestionarea autentificarii
from flask_login import (login_required,#protejeaza paginile care necesita autentificare
                         login_user,    #conecteaza user dupa login
                         logout_user,   #Deconecteaza user
                         current_user   #Return user autentificat
                         )

from werkzeug.security import generate_password_hash #Functie pentru criptarea parolelor

from app import db #Interactionea cu baza de date
from app.forms import DoctorRegistrationForm, PacientRegistrationForm, ProgramarePacientForm  # Formule de inregistrare
from app.models import Appointment, User, Doctor #Modele

main_bp = Blueprint('main', __name__) #Crearea unui Blueprint

#URL-ul principal catre pagina de start index.html
@main_bp.route('/')
def home():
    return render_template('index.html')

#URL-ul catre pagina de inregistrare doctor
@main_bp.route('/register/doctor', methods=['GET', 'POST'])
def register_doctor():
    form = DoctorRegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Acest email este deja utilizat. Alege altul.", "danger")
            return redirect(url_for('main.register_doctor'))

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role="doctor",  # 🔹 Setăm rolul doctor
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        new_doctor = Doctor(
            user_id=new_user.id,
            specialization=form.specialization.data,
            experience=form.experience.data
        )
        db.session.add(new_doctor)
        db.session.commit()

        flash("Contul de doctor a fost creat cu succes! Acum te poți autentifica.", "success")
        return redirect(url_for('main.login_doctor'))

    return render_template("register_doctor.html", form=form)


#URL-ul catre pagina de inregistrare pacient
@main_bp.route('/register/pacient', methods=['GET', 'POST'])
def register_pacient():
    form = PacientRegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Acest email este deja utilizat. Alege altul.", "danger")
            return redirect(url_for('main.register_pacient'))

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role="pacient",  # 🔹 Setăm rolul pacient
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()

        flash("Contul de pacient a fost creat cu succes! Acum te poți autentifica.", "success")
        return redirect(url_for('main.login_pacient'))

    return render_template("register_pacient.html", form=form)

# Permite utilizatorilor sa se deconecteze
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# URL catre linkul de logare pentru doctori
@main_bp.route('/login/personal_medical', methods=['GET', 'POST'])
def login_doctor():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_doctor'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):  # Verifică parola hash-uită
            login_user(user)

            # Verificăm dacă utilizatorul este doctor
            if Doctor.query.filter_by(user_id=user.id).first():
                return redirect(url_for('main.dashboard_doctor'))
            else:
                flash("Nu ai permisiunea de a accesa această secțiune!", "danger")
                return redirect(url_for('main.login_doctor'))

        flash('Autentificare eșuată. Verifică email-ul și parola.', 'danger')

    return render_template('login_doctor.html')


# URL catre linkul de logare pentru pacienti
@main_bp.route('/login/pacient', methods=['GET', 'POST'])
def login_pacient():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_pacient'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):  # Verificăm parola hash-uită
            login_user(user)
            return redirect(url_for('main.dashboard_pacient'))

        flash('Autentificare eșuată. Verifică email-ul și parola.', 'danger')

    return render_template('login_pacient.html')

# URL de programare al pacientilor
@main_bp.route('/programare', methods=['GET', 'POST'])
@login_required
def programare_pacient():
    form = ProgramarePacientForm()
    form.doctor.choices = [(doctor.id, doctor.user.username) for doctor in Doctor.query.all()]  # Populează lista doctorilor

    if form.validate_on_submit():
        try:
            # Creăm programarea cu datele selectate
            appointment_date = datetime.combine(form.date.data, form.time.data)
            new_appointment = Appointment(
                patient_id=current_user.id,
                doctor_id=form.doctor.data,
                date=appointment_date,
                status="pending"
            )
            db.session.add(new_appointment)
            db.session.commit()

            flash("Programarea a fost creată cu succes!", "success")
            return redirect(url_for('main.dashboard_pacient'))

        except Exception as e:
            db.session.rollback()
            flash(f"Eroare la crearea programării: {str(e)}", "danger")

    return render_template("programare_pacient.html", form=form)

@main_bp.route('/programari/doctor', methods=['GET'])
@login_required
def programari_doctor():
    doctor = Doctor.query.filter_by(user_id=current_user.id).first()
    if not doctor:
        flash("Nu ai acces la această pagină.", "danger")
        return redirect(url_for('main.dashboard_pacient'))

    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    return render_template("programari_doctor.html", appointments=appointments)

@main_bp.route('/dashboard/pacient')
@login_required
def dashboard_pacient():
    if current_user.role != "pacient":
        flash("Nu ai acces la această pagină!", "danger")
        return redirect(url_for('main.dashboard_doctor'))

    appointments = Appointment.query.filter_by(patient_id=current_user.id).all()
    return render_template('dashboard_pacient.html', appointments=appointments)



@main_bp.route('/dashboard/doctor')
@login_required
def dashboard_doctor():
    if current_user.role != "doctor":
        flash("Nu ai acces la această pagină!", "danger")
        return redirect(url_for('main.dashboard_pacient'))

    appointments = Appointment.query.filter_by(doctor_id=current_user.id).all()
    return render_template('dashboard_doctor.html', appointments=appointments)


@main_bp.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    # Verifică dacă doctorul curent este responsabil de această programare
    if appointment.doctor.user_id != current_user.id:
        flash("Nu aveți permisiunea să anulați această programare!", "danger")
        return redirect(url_for('main.login_doctor')) #Daca nu are voie sa anuleze sa il directioneze pe pagina de logare

    # Setează statusul programării ca "canceled"
    appointment.status = "canceled"
    db.session.commit()

    flash("Programarea a fost anulată cu succes!", "success")
    return redirect(url_for('main.dashboard_doctor'))


@main_bp.route('/cancel_appointment_pacient/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment_pacient(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    # Verificarepentru a vedea daca utilizatorul conectat este pacientul care a făcut programarea
    if appointment.patient_id != current_user.id:
        flash("Nu aveți permisiunea să anulați această programare!", "danger")
        return redirect(url_for('main.login_pacient'))

    # pune programarea ca fiind "canceled"
    appointment.status = "canceled"
    db.session.commit()

    # Mesaj cum ca a fost anulata programarea
    flash("Programarea a fost anulată cu succes!", "success")
    return redirect(url_for('main.dashboard_pacient')) # revine la dashboard_pacient sa isi poata lua o alta programare


