# Carpe Calendar

The [CarpeStudentem Calendar](https://agenda.carpestudentem.be/calendar/) is a community-driven event calendar designed for the city of Louvain-la-Neuve, Belgium.

![Calendar example](https://github.com/AlexandreDewilde/carpe-calendar/blob/main/doc/images/calendar.png?raw=true)

The primary objective of this project is to foster collaboration by allowing users to add their own events, which will then be reviewed and validated by administrators.

### Technologies Used

The project is built with:

- **Python 3.11**
- **Django** (web framework)
- **SQLite** (database, limited concurrent user support)
- **Bootstrap** (frontend framework)
- **FullCalendar** (JavaScript library for event calendars)

## Installation

To run the project, ensure you have **Python 3.11** or higher installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/AlexandreDewilde/carpe-calendar.git
   cd carpe-calendar
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

## Environment Variables

You need to configure two environment variables:

- `DJANGO_DEBUG`: Set to `0` for production, or `1` for development (debug mode).
- `DJANGO_SECRET_KEY`: Define your secret key for Django.

## Running the Project

To start the development server, use:

```bash
python manage.py runserver
```

## Contributions

Contributions are welcome! Feel free to submit issues, suggestions, open issues, or pull requests to improve the project.
