import sqlite3

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


# Hilfsfunktion, um die Datenbankverbindung aufzubauen
def get_db_connection():
    conn = sqlite3.connect('eventkalender.db')
    conn.row_factory = sqlite3.Row
    return conn

# =================================
# Routen
# =================================
@app.route('/')
@app.route('/')
def home():
    conn = get_db_connection()
    # Alle Events aus der Datenbank abfragen
    events_aus_db = conn.execute('SELECT * FROM events ORDER BY datum ASC').fetchall()
    conn.close()

    # NEU: Wir wandeln die speziellen Row-Objekte in normale Dictionaries um,
    # damit das JavaScript (JSON) im Kalender sie problemlos lesen kann.
    events_liste = [dict(row) for row in events_aus_db]

    return render_template('home.html', events=events_liste)


@app.route('/create', methods=('GET', 'POST'))
def create_event():
    # Wenn der Nutzer auf "Event speichern" klickt, senden wir einen POST-Request
    if request.method == 'POST':
        # Wir greifen die Daten aus den Eingabefeldern ab
        titel = request.form['titel']
        datum = request.form['datum']
        beschreibung = request.form['beschreibung']

        # Wir öffnen die Datenbank und fügen die neuen Daten ein
        conn = get_db_connection()
        conn.execute('INSERT INTO events (titel, datum, beschreibung) VALUES (?, ?, ?)',
                     (titel, datum, beschreibung))
        conn.commit()
        conn.close()

        # Nach dem Speichern leiten wir direkt zurück zur Startseite
        return redirect(url_for('home'))

    # Wenn die Seite ganz normal aufgerufen wird (GET-Request), zeige das leere Formular
    return render_template('add-event.html')


@app.route('/event/<int:event_id>')
def event_detail(event_id):
    conn = get_db_connection()
    # Nur das eine angeklickte Event aus der Datenbank laden
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    conn.close()

    if event:
        return render_template('event.html', event=event)
    else:
        return "Event nicht gefunden", 404


@app.route('/event/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    conn = get_db_connection()
    # Das Event aus der Datenbank löschen
    conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

# =================================
# App start
# =================================

if __name__ == '__main__':
    app.run(debug=True)