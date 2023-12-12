import psycopg2

conn = psycopg2.connect("dbname=scraper user=benhurst")
cur = conn.cursor()


def drop_table(table_name):
    query = f"""DROP TABLE IF EXISTS {table_name};"""
    cur.execute(query)
    conn.commit()


def create_table(table_name, columns):
    query = f"""CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"""
    cur.execute(query)
    conn.commit()


drop_table("indeed_data")
create_table(
    "indeed_data",
    [
        "id SERIAL PRIMARY KEY",
        "raw_id INT",
        "job_title TEXT",
        "company TEXT",
        "location TEXT",
        "type TEXT",
        "salary_start INT",
        "salary_end INT",
        "details TEXT",
        "description TEXT",
        "date_added DATE",
        "search_term TEXT",
        "url TEXT",
    ],
)
