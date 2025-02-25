    # Importăm FlaskForm din biblioteca flask_wtf pentru a crea formulare în Flask
from flask_wtf import FlaskForm

    # Importăm tipurile de câmpuri disponibile în formular
from wtforms import StringField, PasswordField, SubmitField, IntegerField

    # Importăm tipurile speciale de câmpuri pentru selectare și date/oră
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField, TimeField

    # Importăm validatori pentru a ne asigura că utilizatorii introduc date corecte
from wtforms.validators import DataRequired, Email, EqualTo, Length

    # Aici avem formularul de inregistrare doctor
class DoctorRegistrationForm(FlaskForm):
    username = StringField("Nume utilizator", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Parolă", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmă parola", validators=[DataRequired(), EqualTo('password')])
    specialization = StringField("Specializare", validators=[DataRequired()])
    experience = IntegerField("Ani de experiență", validators=[DataRequired()])
    submit = SubmitField("Înregistrează-te")

    # Aici avem formularul de inregistrare pacient
class PacientRegistrationForm(FlaskForm):
    username = StringField("Nume utilizator", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Parolă", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirmă parola", validators=[DataRequired(), EqualTo('password')])
    age = IntegerField("Vârstă", validators=[DataRequired()])
    phone = StringField("Telefon", validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField("Înregistrează-te")

    # Aici avem formularul de inregistrare programarii pacientului
class ProgramarePacientForm(FlaskForm):
    date = DateField("Data programării", validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField("Ora programării", validators=[DataRequired()], format='%H:%M')
    doctor = SelectField("Doctor", validators=[DataRequired()], choices=[])
    submit = SubmitField("Confirmă Programarea")