import psycopg2

conn = psycopg2.connect("dbname=scraper user=benhurst")
cur = conn.cursor()


def drop_table(table_name):
    query = f"""DROP TABLE IF EXISTS {table_name};"""
    cur.execute(query)
    conn.commit()


drop_table("raw_indeed_data")
