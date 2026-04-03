import sqlite3


def search_products(db_path, search_term, category):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # BUG: f-string interpolation allows SQL injection via both parameters
    query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%' AND category = '{category}'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results
