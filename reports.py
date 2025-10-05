import db

# add new report
def add_report(username, title, description, travel_date, country):
    sql = """
        INSERT INTO reports (username, title, content, created_at, country)
        VALUES (?, ?, ?, ?, ?)
    """
    db.execute(sql, [username, title, description, travel_date, country])

# fetch all reports
def get_reports():
    sql = """
        SELECT id, title, content AS description, created_at AS travel_date, country, username
        FROM reports
        ORDER BY id DESC
    """
    print("DEBUG: executing SQL query to fetch reports")
    return db.query(sql, [])

# fetch a report according to id
def get_report(report_id):
    sql = """
        SELECT id, title, content AS description, created_at AS travel_date, country, username
        FROM reports
        WHERE id = ?
    """
    result = db.query(sql, [report_id])
    if result:
        return result[0]
    return None

# update report
def update_report(report_id, title, description, travel_date, country):
    sql = """
        UPDATE reports
        SET title = ?, content = ?, created_at = ?, country = ?
        WHERE id = ?
    """
    db.execute(sql, [title, description, travel_date, country, report_id])

# delete report
def delete_report(report_id):
    sql = "DELETE FROM reports WHERE id = ?"
    db.execute(sql, [report_id])