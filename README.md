# TripTracker
TripTracker is a web application for users to be able to log, classify and share their travel experiences. 

## Features

- Users can create an account and log in.
- Users can add travel reports and edit or delete their own reports.
- Users can browse all reports created by all users.
- Users can search reports by keyword (country or destination).
- Each user has a user page showing their reports and basic statistics.
- Reports can be classified using predefined values (country, holiday type, theme).
- Users can comment on other users’ travel reports.
- Users can upload up to 5 images per report.

## Installation

Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
pip install Flask
```

Create the database tables and insert initial data:

```
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
sqlite3 database.db < countries.sql
```

The init.sql file inserts default classifications (holiday types and themes).  


Run the application:

```
flask run
```

To improve performance when handling larger datasets, a database index was added to the reports table.
The following index is used:
```sql
CREATE INDEX idx_reports_country ON reports(country);
```

## Pylint

Pylint was run with:

pylint app.py

Score: 8.24 / 10

Most warnings were related to:
- Missing docstrings
- Line length limits
- Import order

The report file is included in the repository as `pylint_report.txt`.