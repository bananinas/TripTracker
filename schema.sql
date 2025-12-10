CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT NOT NULL,
    title       TEXT NOT NULL,
    description TEXT NOT NULL,
    travel_date TEXT NOT NULL,
    country     TEXT,
    section     TEXT,
    theme       TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,-- automatically saves date and time of when row was created --
    FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id),
    username TEXT REFERENCES users(username),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE report_classes (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE hotels (
    id INTEGER PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id),
    name TEXT NOT NULL,
    area TEXT
);

CREATE TABLE report_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    FOREIGN KEY (report_id) REFERENCES reports (id)
);

CREATE TABLE countries (
    code TEXT PRIMARY KEY,   -- eg "FI"
    name TEXT NOT NULL       -- eg "Finland"
);



