// Globaler Status für die aktuelle Kalender-Ansicht
let displayDate = new Date();
let currentMonth = displayDate.getMonth();
let currentYear = displayDate.getFullYear();

/**
 * Schaltet zwischen Listen- und Kalenderdarstellung um.
 * Verwendet einfache DOM-Manipulation zur Sichtbarkeitssteuerung.
 */
function switchView(view) {
    if (view === 'list') {
        document.getElementById('view-list').style.display = 'block';
        document.getElementById('view-calendar').style.display = 'none';
        document.getElementById('btn-list').classList.add('active');
        document.getElementById('btn-cal').classList.remove('active');
    } else {
        document.getElementById('view-list').style.display = 'none';
        document.getElementById('view-calendar').style.display = 'block';
        document.getElementById('btn-cal').classList.add('active');
        document.getElementById('btn-list').classList.remove('active');
        renderCalendar();
    }
}

/**
 * Aktualisiert den Monatsspeicher und triggert das Neuzeichnen des Kalenders.
 * Behandelt den Jahreswechsel (Überlauf vom Dezember/Januar).
 */
function changeMonth(step) {
    currentMonth += step;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    } else if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    renderCalendar();
}

/**
 * Kernfunktion: Erzeugt das HTML-Grid für den gewählten Monat.
 * Berechnet den Wochentag des ersten Monatstags und die Anzahl der Tage.
 */
function renderCalendar() {
    const grid = document.getElementById('cal-grid');
    const monthYearLabel = document.getElementById('cal-month-year');

    // Header für Wochentage (statisch)
    const dayNames = `<div class="calendar-day-name">Mo</div><div class="calendar-day-name">Di</div><div class="calendar-day-name">Mi</div><div class="calendar-day-name">Do</div><div class="calendar-day-name">Fr</div><div class="calendar-day-name">Sa</div><div class="calendar-day-name">So</div>`;
    grid.innerHTML = dayNames;

    const monthNames = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"];
    monthYearLabel.innerText = monthNames[currentMonth] + " " + currentYear;

    // Berechnung des ersten Wochentags (angepasst auf Start Montag = 0)
    let firstDay = new Date(currentYear, currentMonth, 1).getDay();
    firstDay = firstDay === 0 ? 6 : firstDay - 1;

    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    // Platzhalter für Tage des Vormonats einfügen
    for (let i = 0; i < firstDay; i++) {
        grid.innerHTML += `<div class="calendar-day empty"></div>`;
    }

    // Tage des aktuellen Monats generieren
    for (let i = 1; i <= daysInMonth; i++) {
        const dayString = i < 10 ? '0' + i : i;
        const monthString = (currentMonth + 1) < 10 ? '0' + (currentMonth + 1) : (currentMonth + 1);
        const dateString = `${currentYear}-${monthString}-${dayString}`;

        /*
           Event-Zuordnung: Prüft für jeden Tag, ob in den geladenen Event-Daten
           ein passender Eintrag für das berechnete Datum existiert.
        */
        let eventHtml = '';
        events.forEach(event => {
            if(event.datum === dateString) {
                eventHtml += `<a href="/event/${event.id}" class="event-badge">${event.titel}</a>`;
            }
        });

        grid.innerHTML += `
            <div class="calendar-day">
                <span class="date-num">${i}</span>
                ${eventHtml}
            </div>
        `;
    }
}
// Initialer Aufruf beim Laden der Seite
renderCalendar();