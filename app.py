from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# =================================
# Ein paar Dummy-Daten.
# =================================
dummy_events = [
    {'id': 1, 'titel': 'Projektmeeting', 'datum': '2026-05-10', 'beschreibung': 'Besprechung der nächsten Schritte.'},
    {'id': 2, 'titel': 'Abteilungsessen', 'datum': '2026-05-15', 'beschreibung': 'Gemeinsames Essen.'}
]

# =================================
# Routen
# =================================
@app.route('/')
def home():
    # Wir übergeben die Events an die Startseite
    return render_template('home.html', events=dummy_events)

@app.route('/create')
def create_event():
    return render_template('add-event.html')


# Route für die Detailansicht eines spezifischen Events
@app.route('/event/<int:event_id>')
def event_detail(event_id):
    # Wir durchsuchen unsere Dummy-Daten nach der passenden ID
    gesuchtes_event = None
    for event in dummy_events:
        if event['id'] == event_id:
            gesuchtes_event = event
            break

    # Wenn wir es gefunden haben, laden wir die Detailseite
    if gesuchtes_event:
        return render_template('event.html', event=gesuchtes_event)
    else:
        return "Event nicht gefunden", 404

    # Route zum Löschen eines Events
@app.route('/event/<int:event_id>/delete', methods=['POST'])
def delete_event(event_id):
    global dummy_events
    # Wir filtern die Liste neu und behalten alle Events, außer dem mit der gelöschten ID
    dummy_events = [e for e in dummy_events if e['id'] != event_id]

    # Danach leiten wir den Nutzer zurück auf die Startseite
    return redirect(url_for('home'))

# =================================
# App start
# =================================

if __name__ == '__main__':
    app.run(debug=True)