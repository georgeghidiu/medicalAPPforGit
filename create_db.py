# Importam create_app din app
from app import create_app

# Importăm db care gestionează baza de date
from app.database import db

# Initializam aplicatia Flask
app = create_app()

# Crează baza de date și tabelele în contextul aplicației
with app.app_context(): # Asigură că baza de date este creată

    db.create_all()     # Aici se creaza toate tabelele din models.py

    print("📌 Tabelele au fost create în `app.db` cu succes!") # Daca au fost create cu succes se afiseaza mesajul

