from flask import Flask, render_template

# hier wird die Flask App initialisiert.
app = Flask(__name__)

# Die Route für die Startseite (die Terminübersicht)
@app.route('/')
def home():
    # Dieser Befehl sucht im "templates" Ordner nach der HTML-Datei für die Startseite
    return render_template('home.html')

# Damit wird der lokalen Server gestartet.
if __name__ == '__main__':
    debug=True # ist extrem hilfreich: Es lädt die Seite automatisch neu, wenn der Code geändert wird
    app.run(debug=True)