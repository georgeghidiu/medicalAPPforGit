from flask import Flask #Importam Flask pentru crearea aplicatiei

from app.config import Config #Importam configuratia aplicatiei din modulul config

from app.database import db #Importam obiectul bazei de date (SQLAlchemy)

from flask_migrate import Migrate #Gestionarea migrărilor bazei de date

from flask_login import LoginManager #Folosim biblioteca Flask-Login si importam LoginManager pentru autentificare și gestionarea sesiunilor utilizatorilor

from app.models import User, Doctor, Appointment # Importăm modelele utilizate în aplicație

# Inițializează extensiile Flask

#Initializare Flask-Migrate
migrate = Migrate()

#Initializare Flask-Login
login_manager = LoginManager()

#Aici cream functia create_app
def create_app():
    app = Flask(__name__, template_folder = "templates")#Cream o instanta a aplicatiei Flask
                                                        # "template_folder = templates" indica locatia fisierelor HTML
    app.config.from_object(Config)     # Configurăm aplicația folosind clasa Config


    # Inițializează baza de date și alte extensii
    db.init_app(app) # Inițializăm baza de date (SQLAlchemy) cu aplicația
    migrate.init_app(app, db) # Inițializăm Flask-Migrate pentru a lega baza de date la mecanismul de migrare
    login_manager.init_app(app) # Inițializăm Flask-Login pentru a gestiona autentificarea utilizatorilor

    login_manager.login_view = "main.login" # Setăm pagina implicită de login pentru utilizatorii neautentificați

    # Înregistrează blueprint-ul
    from app.routes import main_bp #importam blueprint-ul
    app.register_blueprint(main_bp) #Inregistram blueprint-ul

    #  O functie care incarca un utilizator pe baza id-ului
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app  #Returnam aplicatia
