from app.database import conn

def get_articles(id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM articles WHERE article_id = %s", (f'{id}',))
    results = cur.fetchall()

    return results