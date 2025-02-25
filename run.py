from app import create_app #Importam functia create_app din modulul app care va initializa aplicatia noastra Flask
import sys
import os

#LLM - Adaugam directorul curent in sys.path pentru a ne asigura ca putem importa corect modulele din proiect
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = create_app() # Cream un obiect Flask apeland functia create_app

if __name__ == "__main__":
    app.run(debug=True) #Pornim serverul Flask
