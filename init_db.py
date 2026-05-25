import sqlite3

def init_database():
    """
    Initialisiert das Datenbankschema für die Eventverwaltung.
    Erstellt die benötigte Tabelle und fügt initiale Testdaten hinzu (Seeding).
    """
    try:
        # Nutzung des Context Managers für ein absolut sicheres Verbindungsmanagement
        with sqlite3.connect('eventkalender.db') as connection:
            cursor = connection.cursor()

            # Erstellung der Entität 'events' gemäß dem definierten Datenmodell
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titel TEXT NOT NULL,
                    datum TEXT NOT NULL,
                    beschreibung TEXT
                )
            ''')

            # Überprüfen, ob bereits Daten existieren
            # Dies verhindert Duplikate, falls das Skript mehrfach ausgeführt wird
            cursor.execute('SELECT COUNT(*) FROM events')
            if cursor.fetchone()[0] == 0:
                # Eine Liste mit realistischen Testdaten für die Präsentation
                test_events = [
                    ('Team-Meeting: Sprint Planning', '2026-06-15',
                     'Gemeinsame Planung der nächsten Meilensteine und Aufgabenverteilung.'),
                    ('Vorstandssitzung', '2026-06-20', 'Abstimmung über das Budget für das dritte Quartal.'),
                    ('Projekt-Kickoff', '2026-06-10',
                     'Erstes gemeinsames Brainstorming mit allen relevanten Stakeholdern.'),
                    ('Sommerfest Orga-Team', '2026-07-01', 'Besprechung der eingeholten Catering-Angebote.'),
                    ('Kurzes Sync-Meeting', '2026-06-05', '')  # Ein Termin ohne Beschreibung für den Randfall-Test
                ]

                # executemany fügt die gesamte Liste effizient auf einmal ein
                cursor.executemany("INSERT INTO events (titel, datum, beschreibung) VALUES (?, ?, ?)", test_events)
                print("Erfolgreich 5 Testevents angelegt.")
            else:
                print("Die Tabelle enthält bereits Daten. Seeding wurde übersprungen.")

            connection.commit()
            print("Datenbankschema wurde erfolgreich initialisiert!")

    except sqlite3.Error as e:
        print(f"Ein Fehler bei der Datenbankinitialisierung ist aufgetreten: {e}")

if __name__ == '__main__':
    init_database()