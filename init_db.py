import sqlite3

# Verbindung herstellen (die Datei wird automatisch erstellt, falls sie fehlt)
connection = sqlite3.connect('eventkalender.db')
cursor = connection.cursor()

# Die Tabelle 'events' erstellen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titel TEXT NOT NULL,
        datum TEXT NOT NULL,
        beschreibung TEXT
    )
''')

# Einen ersten echten Test-Eintrag hinzufügen
cursor.execute("INSERT INTO events (titel, datum, beschreibung) VALUES (?, ?, ?)",
            ('Erstes echtes Datenbank-Event', '2026-05-20', 'Dieser Termin kommt direkt aus SQLite!'))

# Speichern und schließen
connection.commit()
connection.close()

print("Datenbank und Tabelle wurden erfolgreich erstellt!")