from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

import scrpy.base.connections as settings

Base = declarative_base()

DATABASE = {
    "drivername": "postgres",
    "host": settings.PG_HOST,
    "port": settings.PG_PORT,
    "username": settings.PG_USER,
    "password": settings.PG_PASSWORD,
    "database": settings.PG_DBNAME,
}
DATABASE_URL = "postgresql://"+settings.PG_USER+\
                    ":"+settings.PG_PASSWORD+"@"+settings.PG_HOST+\
                    ":"+settings.PG_PORT+"/"+settings.PG_DBNAME

def db_connect() -> Engine:
    return create_engine(DATABASE_URL, encoding="utf8", echo=False)