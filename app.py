from flask import Flask, render_template, request, redirect, url_for, flash, abort
import sqlite3
from datetime import datetime

app = Flask(__name__)
# Kryptografischer Schlüssel für das Session Management (Flash Messages)
app.secret_key = 'ein_sehr_geheimer_schluessel_fuer_mein_projekt'


# =================================
# Datenbanklogik (Model)
# =================================
def get_db_connection():
    """Baut die Verbindung zur SQLite Datenbank auf und konfiguriert die Zeilenstruktur."""
    conn = sqlite3.connect('eventkalender.db')
    conn.row_factory = sqlite3.Row
    return conn

# =================================
# Controller & Routing
# =================================

@app.route('/')
def home():
    """Lädt alle Events chronologisch sortiert und rendert die Startseite."""
    conn = get_db_connection()
    events_aus_db = conn.execute('SELECT * FROM events ORDER BY datum ASC').fetchall()
    conn.close()

    # Umwandlung der Row Objekte in Dictionaries für die nahtlose JSON Verarbeitung im Frontend
    events_liste = [dict(row) for row in events_aus_db]

    return render_template('home.html', events=events_liste)


@app.route('/create', methods=('GET', 'POST'))
def create_event():
    """Steuert die Erstellung neuer Events inklusive serverseitiger Validierung."""
    if request.method == 'POST':
        # Whitespaces entfernen, um leere Eingaben zu vermeiden
        titel = request.form['titel'].strip()
        datum = request.form['datum']
        beschreibung = request.form['beschreibung'].strip()

        # Validierungsregel 1: Pflichtfelder prüfen
        if not titel or not datum:
            flash('Titel und Datum sind Pflichtfelder!', 'error')
            return redirect(url_for('create_event'))

        # Validierungsregel 2: Datumsformat und zeitliche Logik prüfen
        try:
            eingabe_datum = datetime.strptime(datum, '%Y-%m-%d').date()
            heute = datetime.today().date()

            if eingabe_datum < heute:
                flash('Das Datum darf nicht in der Vergangenheit liegen!', 'error')
                return redirect(url_for('create_event'))

        except ValueError:
            # Fängt manipulierte POST Requests ab, falls das Frontend umgangen wurde
            flash('Ungültiges Datumsformat!', 'error')
            return redirect(url_for('create_event'))

        # Speicherung in der Datenbank mittels Prepared Statements (Schutz vor SQL Injection)
        conn = get_db_connection()
        conn.execute('INSERT INTO events (titel, datum, beschreibung) VALUES (?, ?, ?)',
                     (titel, datum, beschreibung))
        conn.commit()
        conn.close()

        flash('Event erfolgreich erstellt!', 'success')
        return redirect(url_for('home'))

    return render_template('add-event.html')


@app.route('/event/<int:event_id>')
def event_detail(event_id):
    """Lädt die Detailansicht eines spezifischen Geschäftsobjekts."""
    conn = get_db_connection()
    event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    conn.close()

    if event:
        return render_template('event.html', event=event)
    else:
        # Löst den Errorhandler aus, falls eine ungültige ID aufgerufen wird
        abort(404)


@app.route('/event/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    """Löscht ein Event sicher aus der Datenbank."""
    conn = get_db_connection()
    conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()

    flash('Das Event wurde erfolgreich gelöscht.', 'success')
    return redirect(url_for('home'))


# =================================
# Fehlerbehandlung
# =================================

@app.errorhandler(404)
def page_not_found(e):
    """Zentrale Fehlerseite für nicht gefundene Ressourcen."""
    return render_template('404.html'), 404


# =================================
# Applikationsstart
# =================================

if __name__ == '__main__':
    app.run(debug=True)