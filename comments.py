import db

def add_comment(report_id, username, content):
    db.execute("INSERT INTO comments (report_id, username, content) VALUES (?, ?, ?)",
               [report_id, username, content])

def get_comments(report_id):
    return db.query("SELECT * FROM comments WHERE report_id = ? ORDER BY created_at", [report_id])

def delete_comment(comment_id, username):
    db.execute("DELETE FROM comments WHERE id=? AND username=?", [comment_id, username])

def get_comments_by_user(username):
    sql = """
        SELECT c.id, c.report_id, c.content, c.created_at, r.title
        FROM comments c
        JOIN reports r ON c.report_id = r.id
        WHERE c.username = ?
        ORDER BY c.created_at DESC
    """
    return db.query(sql, [username])