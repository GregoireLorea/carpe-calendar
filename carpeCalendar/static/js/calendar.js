const colors = {};

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
        },
        locale: 'fr',
        firstDay: 1,
        headerToolbar: {
            left: 'addEvent',
            center: 'title',
            right: 'dayGridDay,dayGridWeek,dayGridMonth,listMonth prev,next',
        },
        buttonText: {
            month: 'Mois',
            listMonth: "Liste",
            week: 'Semaine',
            day: 'Jour',
            today: 'Aujourd\'hui',

        },
        navLinks: true,
        navLinkDayClick: function(date) {
            calendar.changeView('dayGridDay', date.toISOString());
        },
        height: 'auto',
        eventBorderColor: 'black',
        titleFormat: { day: 'numeric', year: 'numeric', month: 'long' },
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
            if (!element.checked || !placeElement.checked) {
                arg.el.style.display = "none";
            }
            // if (arg.view.type !== "listMonth") {
                arg.el.style.backgroundColor = colors[arg.event.extendedProps.saved_location.name];
            // }
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
}

document.addEventListener('DOMContentLoaded', function() {
    initPlaceColors();
    createCalendar();
});