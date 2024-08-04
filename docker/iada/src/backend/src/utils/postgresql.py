import os
import psycopg2.pool

db_url = (
    os.environ.get("POSTGRESQL_URL") or "postgres://postgres:postgres@localhost:5432/iada"
)

pool = psycopg2.pool.SimpleConnectionPool(
    2,
    3,
    database=db_url.split("/")[-1],
    host=db_url.split("@")[1].split(":")[0],
    user=db_url.split("://")[1].split(":")[0],
    password=db_url.split("://")[1].split(":")[1].split("@")[0],
    port=db_url.split("@")[1].split(":")[1].split("/")[0],
)
