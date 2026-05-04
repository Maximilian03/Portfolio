from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
# Ein geheimer Schlüssel für die Flash Messages
app.secret_key = 'ein_sehr_geheimer_schluessel_fuer_mein_projekt'


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
    if request.method == 'POST':
        # .strip() entfernt versehentliche Leerzeichen am Anfang und Ende
        titel = request.form['titel'].strip()
        datum = request.form['datum']
        beschreibung = request.form['beschreibung'].strip()

        # Die Validierung (Pflichtfelder und Vergangenheit)
        if not titel or not datum:
            flash('Titel und Datum sind Pflichtfelder!', 'error')
            return redirect(url_for('create_event'))

        # Wir wandeln den Text aus dem Formular in ein echtes Datum um
        try:
            eingabe_datum = datetime.strptime(datum, '%Y-%m-%d').date()
            heute = datetime.today().date()

            # Jetzt vergleichen wir die beiden Daten
            if eingabe_datum < heute:
                flash('Das Datum darf nicht in der Vergangenheit liegen!', 'error')
                return redirect(url_for('create_event'))

        except ValueError:
            # Falls jemand versucht, das HTML zu manipulieren und ein falsches Format schickt
            flash('Ungültiges Datumsformat!', 'error')
            return redirect(url_for('create_event'))

        conn = get_db_connection()
        conn.execute('INSERT INTO events (titel, datum, beschreibung) VALUES (?, ?, ?)',
                     (titel, datum, beschreibung))
        conn.commit()
        conn.close()

        # Erfolgsmeldung nach dem Speichern
        flash('Event erfolgreich erstellt!', 'success')
        return redirect(url_for('home'))

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
    conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()

    # NEU: Erfolgsmeldung nach dem Löschen
    flash('Das Event wurde gelöscht.', 'success')
    return redirect(url_for('home'))


# =================================
# App start
# =================================

if __name__ == '__main__':
    app.run(debug=True)