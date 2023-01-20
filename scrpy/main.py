import subprocess
import base.connections as settings
import psycopg2
from psycopg2 import extras
import csv

PG_DSN = f"dbname={settings.PG_DBNAME} user={settings.PG_USER} password={settings.PG_PASSWORD} host={settings.PG_HOST} port={settings.PG_PORT}"
conn = psycopg2.connect(PG_DSN, cursor_factory=extras.RealDictCursor)

with conn.cursor() as cursor:
    try:
        cursor.execute('''DROP TABLE nouts;''')
        conn.commit()  
    except Exception as e:
        print ("Таблицы нет в БД. Едем дальше")
conn.close()
conn = psycopg2.connect(PG_DSN, cursor_factory=extras.RealDictCursor)
with conn.cursor() as cursor:
    cursor.execute('''CREATE TABLE nouts (
        id serial4 NOT NULL,
        url varchar NULL,
        "date" varchar NULL,
        "name" varchar NULL,
        processor varchar NULL,
        core int4 NULL,
        mhz float8 NULL,
        ram int4 NULL,
        screen float8 NULL,
        price int4 NULL,
        "rank" float8 NULL,
        CONSTRAINT nouts_pkey PRIMARY KEY (id),
        CONSTRAINT nouts_url_key UNIQUE (url)
    );''')
    conn.commit()  
    conn.close()

# subprocess.run("scrapy crawl nout", shell=True)      
# subprocess.run("scrapy crawl nout2", shell=True)
subprocess.run("scrapy runspider spider/nout.py", shell=True)      
     

conn = psycopg2.connect(PG_DSN, cursor_factory=extras.RealDictCursor)
with conn.cursor() as cursor:
    result=[['ID', 'NAME', 'DATE', 'PROCESSOR', 'RAM', 'SCREEN', 'allCPU_mhz', 'PRICE', 'RANK', 'URL']]
    cursor.execute('''SELECT id, "name", "date", processor, ram, screen, mhz, price, "rank", url
                    FROM nouts
                    ORDER BY "rank" DESC
                    LIMIT 5;
        ''')
    for i in cursor:
        result.append([i["id"] , i["name"], i["date"], i["processor"], i["ram"], i["screen"], i["mhz"], i["price"], i["rank"], i["url"]])
        with open('result.csv', "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(result)
conn.close()