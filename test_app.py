import unittest
from app import app


class EventkalenderTests(unittest.TestCase):
    """Test Suite für die Validierung der Kernfunktionen des Eventkalenders."""

    def setUp(self):
        """
        Initialisiert die Testumgebung vor jedem einzelnen Testlauf.
        Erstellt einen virtuellen Test Client (Mocking), um HTTP Requests zu simulieren.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_startseite_erreichbar(self):
        """Testet, ob der Controller für die Startseite korrekt antwortet."""
        antwort = self.app.get('/')

        # HTTP 200 (OK) verifiziert die erfolgreiche Routenauflösung und das Rendering
        self.assertEqual(antwort.status_code, 200)

    def test_erstellen_seite_erreichbar(self):
        """Prüft die Erreichbarkeit des Eingabeformulars für neue Events."""
        antwort = self.app.get('/create')

        self.assertEqual(antwort.status_code, 200)

    def test_event_nicht_gefunden_404(self):
        """
        Testet die Fehlerbehandlung (Exception Handling) der Anwendung.
        Der Aufruf eines nicht existierenden Geschäftsobjekts muss zwingend HTTP 404 liefern.
        """
        antwort = self.app.get('/event/9999')

        # HTTP 404 (Not Found) bestätigt die korrekte Fehlerkapselung
        self.assertEqual(antwort.status_code, 404)


if __name__ == '__main__':
    unittest.main()