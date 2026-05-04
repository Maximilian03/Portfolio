import unittest
from app import app


class EventkalenderTests(unittest.TestCase):

    def setUp(self):
        # Es wird ein virtuellen Client, der Nutzerverhalten simuliert erstellt.
        self.app = app.test_client()
        self.app.testing = True

    def test_startseite_erreichbar(self):
        # Der virtuelle Client ruft die Hauptseite auf
        antwort = self.app.get('/')
        print("Test 1/3")

        # Wir erwarten den Statuscode 200 (Das bedeutet im Web: Alles OK)
        self.assertEqual(antwort.status_code, 200)

    def test_erstellen_seite_erreichbar(self):
        # Testet, ob das Formular fehlerfrei geladen wird
        antwort = self.app.get('/create')
        self.assertEqual(antwort.status_code, 200)
        print("Test 2/3")

    def test_event_nicht_gefunden_404(self):
        # Testet unsere Fehlerbehandlung: Was passiert bei einer falschen Event-ID?
        antwort = self.app.get('/event/9999')
        # Wir erwarten hier explizit den Fehler 404 (Not Found)
        self.assertEqual(antwort.status_code, 404)
        print("Test 3/3")


if __name__ == '__main__':
    unittest.main()