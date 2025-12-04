import db

def add_hotels(report_id, hotels_clean):
    # hotels_clean on lista (name, area) -tuplia
    sql = "INSERT INTO hotels (report_id, name, area) VALUES (?, ?, ?)"
    for name, area in hotels_clean:
        db.execute(sql, [report_id, name, area])

def get_hotels(report_id):
    sql = "SELECT name, area FROM hotels WHERE report_id = ?"
    return db.query(sql, [report_id])
