CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
-- Tämä luo taulun new_reportiin
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    username TEXT NOT NULL,
    travel_date TEXT,
    FOREIGN KEY(username) REFERENCES users(username)
);

CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- automatically saves date and time of when row was created --
    country TEXT,
    FOREIGN KEY(username) REFERENCES users(username)
);
