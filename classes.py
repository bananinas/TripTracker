import db

def get_holiday_types():
    return db.query("SELECT value FROM classes WHERE title='Holiday type' ORDER BY value", [])

def get_themes():
    return db.query("SELECT value FROM classes WHERE title='Theme' ORDER BY value", [])

def get_countries():
    sql = "SELECT code, name FROM countries ORDER BY name"
    return db.query(sql, [])


