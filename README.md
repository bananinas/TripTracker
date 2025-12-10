# TripTracker
A simple app to log and share travel experiences.

- Users can create an account and log in.
- Users can add travel reports, and edit or delete their own reports.
- Users can view all travel reports added by themselves and other users.
- Users can search travel reports by keyword or other criteria.
- The application has user pages that show statistics and all reports created by each user.
- Users can classify each travel report using predefined classifications (such as country, holiday type and theme).
- Users can comment on other users’ travel reports.

## Installation

Install Flask:

```
$ pip install Flask
```

Create the database tables and insert initial data:

```
$ sqlite3 database.db < schema.sql
```

Run the application:

```
$ flask run
```

To improve performance when handling larger datasets, a database index was added to the reports table.
The following index is used:
CREATE INDEX idx_reports_country ON reports(country);

## Pylint

Pylint was run with:

pylint app.py

Score: 8.24 / 10

Most warnings were related to:
- Missing docstrings
- Line length limits
- Import order

The report file is included in the repository as `pylint_report.txt`.