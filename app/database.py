import psycopg2
import os
from psycopg2.extras import execute_values

def connect_to_db():
    """
    This function connects to the database.
    Returns:
    conn: psycopg2 connection
    """
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        port=os.environ['DB_PORT']
    )
    return conn

conn = connect_to_db()

def write_result_to_db(conn, article_id, values):
    """
    This function writes the result to the database.
    If the data already exists, it will not be written.
    Parameters:
    conn: psycopg2 connection
    values: list
    
    Returns:
    None
    """
    # Check if data with the same article_id and similar_article_id already exists
    with conn.cursor() as cur:
        cur.execute("SELECT article_id, similar_article_id FROM articles where article_id = %s", (str(article_id),))
        
        existing_data = cur.fetchall()
    
    existing_data = set(existing_data)
    
    if existing_data:
        return None

    with conn.cursor() as cur:
        insert_sql = "INSERT INTO articles (article_id, similar_article_id, title, url, similarity) VALUES %s"
        execute_values(cur, insert_sql, [tuple(v.values()) for v in values])
    
    conn.commit()
