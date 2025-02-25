Acest `README.md` include toate informațiile necesare:

🐍🐍🐍🐍    PYTHON    🐍🐍🐍🐍

O aplicatie medicala - Flask App 

Ce face proiectul? – Descriere
Acest proiect este o aplicație web construită cu Flask, Flask-Login și SQLAlchemy 
care permite:
    Doctorilor      - să gestioneze programările pacienților.
    Pacienților     - să își rezerve consultații medicale.

Ce tehnologii sunt folosite?
Backend: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login
    Baza de date:   SQLite
    Front-end:      HTML, CSS - BootStrap, Jinja2

Cum este structurat proiectul?
    
medical_app/🐍
│── 🗂️app/                   # Directorul principal al aplicației Flask
│   ├── 🗂️templates/         # Fisierele HTML
│   │   ├── 👉base.html
│   │   ├── 👉index.html
│   │   ├── 👉login_pacient.html
│   │   ├── 👉login_doctor.html
│   │   ├── 👉register_pacient.html
│   │   ├── 👉register_doctor.html
│   │   ├── 👉dashboard_pacient.html
│   │   ├── 👉dashboard_doctor.html
│   │   ├── 👉programari_doctor.html
│   │   ├── 👉programare_pacient.html
│   ├── 🗂️static/            # CSS, imagini, JS
│   │   ├── 👉styles.css
│   │   ├── 👉script.js
│   ├── 👉routes.py          # Definirea tuturor rutelor (ex: login, register, dashboard)
│   ├── 👉models.py          # Definirea modelelor bazei de date
│   ├── 👉forms.py           # Formulare pentru autentificare și înregistrare
│   ├── 👉database.py        # Configurarea bazei de date
│   ├── 👉__init__.py        # Inițializarea aplicației Flask
│   ├── 👉config.py          # Configurația aplicației (ex: secret key, baza de date)
│── 🗂️migrations/            # Folder pentru Flask-Migrate
│── 🗂️instance/              # Folder unde se salvează baza de date SQLite
│   ├── 👉app.db             # Fișierul bazei de date SQLite
│── 👉create_db.py           # Script pentru crearea bazei de date
│── 👉run.py                 # Fișierul principal pentru a porni serverul Flask
│── 📄requirements.txt       # Lista dependențelor Python
│── 📄README.md              # Documentația proiectului



Ce funcționalități există?
    Doctorii și pacienții se pot înregistra separat
    Parolele sunt securizate folosind hashing (werkzeug.security)
    Sesiunea este gestionată cu Flask-Login si UserMixin pentru a menține utilizatorii autentificați
    Dashboard-uri separate pentru Doctori si Pacienti
    Pacientii se pot programa la un anumit doctor disponibil selectand data si ora programarii
    Doctorii pot vedea programarile
    Utilizatorii(doctori/pacienti) se pot deconecta

Ce as dori sa adaug pe viitor?

**Doctor:**
Un calendar pentru dashboard-ul doctorilor(sa fie agenda lor medicala)
Sa poata schimba view-ul calendarului:
- sa vada o singura zi, o saptamana etc
Sa vada numarul pacientilor pe care ii are intr-o zi sau intr-o saptamana
Sa poata anula o zi intreaga cu un singur mesaj de grup pentru pacientii din acea zi

**Pacient:**
 - sa isi poata alege un doctor in functie de locatie sau chiar in functie de patologia pe care o are 
 - istoric ale programarilor
    
pip install -r requirements.txt in bash pentru instalarea tuturor modulelor