import sqlite3


def get_user(db_path, username):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # BUG: string concatenation allows SQL injection
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result


def authenticate(db_path, username, password):
    user = get_user(db_path, username)
    if user and user[2] == password:
        return True
    return False
