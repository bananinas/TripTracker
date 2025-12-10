import db

def get_reports():
    sql = "SELECT * FROM reports ORDER BY created_at DESC"
    return db.query(sql)


def get_report(id):
    sql = """
        SELECT id, username, title, description, created_at,
               country, travel_date, section, theme
        FROM reports
        WHERE id = ?
    """
    result = db.query(sql, [id])
    return result[0] if result else None


def add_report(username, title, description, travel_date, country, section, theme):
    sql = """
        INSERT INTO reports
            (username, title, description, travel_date, country, section, theme)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    params = [username, title, description, travel_date, country, section, theme]
    report_id = db.execute(sql, params, return_lastrowid=True)
    return report_id


def update_report(report_id, title, description, travel_date, country, section, theme):
    sql = """
        UPDATE reports
        SET title = ?,
            description = ?,   
            travel_date = ?,
            country = ?,
            section = ?,
            theme = ?
        WHERE id = ?
    """
    params = [title, description, travel_date, country, section, theme, report_id]
    db.execute(sql, params)

def delete_report(report_id, username):
    db.execute("DELETE FROM report_images WHERE report_id = ?", [report_id])
    db.execute("DELETE FROM comments WHERE report_id = ?", [report_id])
    sql = "DELETE FROM reports WHERE id = ? AND username = ?"
    db.execute(sql, [report_id, username])

def get_images(report_id):
    sql = "SELECT id, filename FROM report_images WHERE report_id = ?"
    return db.query(sql, [report_id])

def delete_image(image_id, username):
    sql = """
        DELETE FROM report_images
        WHERE id = ?
        AND report_id IN (SELECT id FROM reports WHERE username = ?)
    """
    db.execute(sql, [image_id, username])
