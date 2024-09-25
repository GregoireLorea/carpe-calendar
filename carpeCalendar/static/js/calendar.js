const colors = {};

const accessibility_list = ["blind_friendly", "deaf_friendly", "pmr_friendly", "neurodiversity_friendly"];

const randomColors = [
    "#E3826F",
    "#E4A9A4",
    "#EFBA97",
    "#F1CCBB",
    "#E7D5C7",
];

function initPlaceColors() {
    for (place of places) {
        colors[place] = randomColors[Math.floor(Math.random() * randomColors.length)];
        const dot = document.getElementById("dot-" + place);
        dot.style.backgroundColor = colors[place];
    }
}

function createCalendar() {
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        themeSystem: 'bootstrap5',
        initialView: screen.width > 800 ? 'dayGridWeek' : 'dayGridDay',
        customButtons: {
            addEvent: {
                text: 'Ajouter un événement',
                click: function() {
                    location.href = "/add-event";
                }
            },
            today: {
                text: 'Aujourd\'hui',
                click: function() {
                    calendar.today();
                }
            }
        },
        locale: 'fr',
        firstDay: 1,
        headerToolbar: {
            left: 'addEvent',
            center: 'title',
            right: 'dayGridDay,dayGridWeek,dayGridMonth,listMonth prev,today,next',
        },
        buttonText: {
            month: 'Mois',
            listMonth: "Liste",
            week: 'Semaine',
            day: 'Jour',
            today: 'Aujourd\'hui',

        },
        navLinks: true,
        nextDayThreshold: '06:00:00',
        navLinkDayClick: function(date) {
            calendar.changeView('dayGridDay', date.toISOString());
        },
        height: 'auto',
        eventBorderColor: 'black',
        titleFormat: { day: 'numeric', year: 'numeric', month: 'long' },
        eventTimeFormat: { hour: 'numeric', minute: '2-digit', hour12: false },
        eventDisplay: 'block',
        eventBorderColor: 'gray',
        eventSources : [
            {
                url: "/events",
            }
        ],
        eventClick: function(info) {
            location.href = "/event/" + info.event.id;
        },
        eventDidMount: function(arg) {
            const element = document.getElementById("checkbox-" + arg.event.extendedProps.category.name);
            const placeElement = document.getElementById("checkbox-place-" + arg.event.extendedProps.saved_location.name);
            let display = false;
            let atLeastOneChecked = false;
            for (accessibility of accessibility_list) {
                const accessibilityElement = document.getElementById("checkbox-" + accessibility);
                atLeastOneChecked |= accessibilityElement.checked;
                if (arg.event.extendedProps[accessibility] && accessibilityElement.checked) {
                    display = true;
                }
            }
            display |= !atLeastOneChecked;
            display &= (element.checked && placeElement.checked);
            if (!display) {
                arg.el.style.display = "none";
            }

            const dotEl = arg.el.getElementsByClassName('fc-list-event-dot')[0];
            if (dotEl) {
                dotEl.style.borderColor = colors[arg.event.extendedProps.saved_location.name];
                // dotEl.style.backgroundColor = colors[arg.event.extendedProps.saved_location.name];
            }
            else {
                arg.el.style.backgroundColor = colors[arg.event.extendedProps.saved_location.name];
            }

            if (screen.width > 900 && arg.view.type !== "listMonth") {
                const span = document.createElement("span");
                span.textContent = "📍" + arg.event.extendedProps.location;
                arg.el.getElementsByClassName("fc-event-main-frame")[0].append(span);
            }
            arg.el.style.cursor = "pointer";
        },
    });
    calendar.render();
    for (category of categories) {
        document.getElementById("checkbox-" + category).addEventListener("change", function() {
            calendar.refetchEvents();
        });
    }
    for (place of places) {
        document.getElementById("checkbox-place-" + place).addEventListener("change", function() {
            calendar.refetchEvents();
        });
    }

    for (accessibility of accessibility_list) {
        document.getElementById("checkbox-" + accessibility).addEventListener("change", function() {
            calendar.refetchEvents();
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initPlaceColors();
    createCalendar();
});