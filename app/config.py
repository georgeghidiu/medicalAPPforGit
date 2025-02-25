import os #Importa modulul os. os interactioneaza cu sistemul de fisiere si variabile de mediu

#Obtine calea absoluta a directorului radacina. Aveam o eroare si AI-ul mi-a pus linia asta de cod si a mers
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


#Defineste o clasa de configurare pentru aplicatia Flask
class Config:
    # SECRET_KEY este utilizat de Flask pentru a securiza sesiunile utilizatorilor și protecția CSRF
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key")

    # Seteaza calea bazei de date SQLite
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'app.db')}"

    # Dezactiveaza notificarile pentru modificarile facut in baza de date
    SQLALCHEMY_TRACK_MODIFICATIONS = False
