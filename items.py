import db

def add_item(username, title, description, travel_date):
    sql = "INSERT INTO items (username, title, description, travel_date) VALUES (?, ?, ?, ?)"
    db.execute(sql, [username, title, description, travel_date])

def get_items():
    sql = "SELECT id, title, description, travel_date, username FROM items ORDER BY id DESC"
    return db.query(sql)

def get_report(report_id):
    sql = """SELECT items.id,
                    items.title,
                    items.description,
                    items.travel_date,
                    users.username
             FROM items
             JOIN users ON items.username = users.username
             WHERE items.id = ?"""
    result = db.query(sql, [report_id])
    if result:
        return result[0]
    return None

def update_report(report_id, title, description, travel_date):
    sql = "UPDATE items SET title=?, description=?, travel_date=? WHERE id=?"
    db.execute(sql, [title, description, travel_date, report_id])

def delete_report(report_id):
    sql = "DELETE FROM items WHERE id=?"
    db.execute(sql, [report_id])