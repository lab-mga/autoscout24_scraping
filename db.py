import cx_Oracle

# Crear pool al iniciar la app
dsn = cx_Oracle.makedsn("localhost", 1521, service_name="XEPDB1")
pool = cx_Oracle.SessionPool(
    user="dbscrapper",
    password="Q1w2e3r4",
    dsn=dsn,
    min=1,
    max=5,
    increment=1,
    threaded=True,
    getmode=cx_Oracle.SPOOL_ATTRVAL_WAIT
)

def get_connection():
    return pool.acquire()