from flask_sqlalchemy import SQLAlchemy # importam SQLAlchemy

db = SQLAlchemy() #Cream  o instanta a obiectului SQLAlchemy si este initializata in create_app.py(db.init_app(app))

#Initializarea bazei de date
def init_app(app):
    db.init_app(app) #Legatura dintre db si app

