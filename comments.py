import db

def add_comment(report_id, username, content):
    db.execute(
        "INSERT INTO comments (report_id, username, content) VALUES (?, ?, ?)",
        [report_id, username, content]
    )

def get_comments(report_id):
    sql = """
        SELECT id, report_id, username, content, created_at
        FROM comments
        WHERE report_id = ? AND status = 1
        ORDER BY created_at DESC
    """
    return db.query(sql, [report_id])

def delete_comment(comment_id, username):
    sql = "UPDATE comments SET status = 0 WHERE id = ? AND username = ?"
    db.execute(sql, [comment_id, username])
def get_comments_by_user(username):
    sql = """
        SELECT c.id, c.report_id, r.title, c.content, c.created_at
        FROM comments c
        JOIN reports r ON c.report_id = r.id
        WHERE c.username = ? AND c.status = 1
        ORDER BY c.created_at DESC
    """
    return db.query(sql, [username])
