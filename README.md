# Eventkalender Webanwendung

Eine leichtgewichtige, auf Flask basierende Webanwendung zur Verwaltung von Terminen. Dieses Projekt wurde im Rahmen des Moduls Software Engineering entwickelt und demonstriert eine saubere Architektur, sichere Datenbankanbindung und eine dynamische Benutzeroberfläche.

## Projektübersicht

Die Applikation ermöglicht es Benutzern, neue Events anzulegen, diese in einer Datenbank zu speichern und übersichtlich anzeigen zu lassen. Dabei wurde großer Wert auf Nutzerfreundlichkeit, Datensicherheit und Codequalität gelegt. Der Quellcode umfasst kompakte und gut strukturierte 550 Zeilen.

## Kernfunktionen

* **Dynamische Ansichten:** Nahtloser Wechsel zwischen einer interaktiven Kalenderansicht (Standard) und einer detaillierten Listenansicht ohne Neuladen der Seite.
* **Robuste Datenbank:** Zuverlässige und dauerhafte Speicherung aller Termine über SQLite.
* **Eingabevalidierung:** Serverseitige Prüfung auf Pflichtfelder sowie die Blockierung von Terminen, die in der Vergangenheit liegen.
* **Direktes Nutzerfeedback:** Visuelle Erfolgsmeldungen und Fehlermeldungen (Flash Messages) führen den Anwender durch die App.
* **Hohe Sicherheit:** Vollständiger Schutz vor SQL Injections durch die konsequente Nutzung von Prepared Statements.
* **Eigene Fehlerseiten:** Benutzerdefinierte und gestaltete 404 Fehlerseite zur besseren Orientierung bei falschen URLs.
* **Qualitätssicherung:** Integrierte automatisierte Unit Tests für die wichtigsten Funktionen und Routen.

## Technologie Stack

* **Backend:** Python, Flask, SQLite3
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Testumgebung:** Python unittest

## Lokales Setup und Installation

Befolge diese Schritte, um das Projekt lokal auf deinem Rechner auszuführen:

1. **Repository klonen:** Lade den Projektordner auf deinen Computer herunter.
2. **Abhängigkeiten installieren:** Stelle sicher, dass Python installiert ist, und installiere Flask über das Terminal mit dem Befehl: `pip install flask`
3. **Datenbank initialisieren:** Führe einmalig das Skript zur Erstellung der Datenbank aus. Tippe dazu ins Terminal: `python init_db.py`
4. **Server starten:** Starte die Hauptanwendung mit dem Befehl: `python app.py`
5. **App öffnen:** Öffne deinen Webbrowser und rufe die Adresse `http://127.0.0.1:5000` auf.

## Testing

Das Projekt enthält eine eigene Testumgebung, um die fehlerfreie Funktion der Kernrouten sicherzustellen. 
Um die Tests auszuführen, gib folgenden Befehl in dein Terminal ein:
`python -m unittest test_app.py`