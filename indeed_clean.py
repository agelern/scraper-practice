import logging, psycopg2, os, re

log = logging.getLogger()
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=os.environ.get("LOGLEVEL", "INFO"),
    datefmt="%Y-%m-%d %H:%M:%S",
)

conn = psycopg2.connect("dbname=scraper user=benhurst")
cur = conn.cursor()


def fetch_data(table_name):
    query = f"""SELECT * FROM {table_name}"""
    cur.execute(query)
    rows = cur.fetchall()
    return rows


def clean(rows):
    for each in rows:
        if each[5] != "NULL":
            pay_and_type = each[5].split("e.")[1].split("Job type")
            if len(pay_and_type) != 1:
                # print(pay_and_type)
                pay = pay_and_type[0].strip()
                type = pay_and_type[1].strip()
            else:
                type = pay_and_type[0].strip()
            print(pay)
    # print(each[5])


rows = fetch_data("raw_indeed_data")
clean(rows)
