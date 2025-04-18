import oracledb
import atexit


db_user = "dbscrapper"
db_password = "Q1w2e3r4"
# El DSN para modo Thin es generalmente "host:port/service_name"
db_dsn = "localhost:1522/XEPDB1"

# Inicializar el cliente Oracle (opcional para modo Thin, pero buena práctica)
# Si no se especifica lib_dir, usará el modo Thin por defecto.
# Comentado para forzar modo Thin si no hay Instant Client instalado
# try:
#     oracledb.init_oracle_client()
# except Exception as e:
#     print(f"Error initializing Oracle client: {e}")
#     # Considera si quieres detener la aplicación aquí o continuar
#     pass

# Crear pool al iniciar la app usando oracledb
try:
    pool = oracledb.create_pool(
        user=db_user,
        password=db_password,
        dsn=db_dsn,
        min=1,
        max=5,
        increment=1,
        # getmode=oracledb.POOL_GETMODE_WAIT # Equivalente a SPOOL_ATTRVAL_WAIT
        # Nota: POOL_GETMODE_WAIT es el modo por defecto en create_pool
    )
    print("Connection pool created successfully.")
except Exception as e:
    print(f"Error creating connection pool: {e}")
    # Manejar el error apropiadamente, quizás salir de la aplicación
    pool = None # Asegurarse de que pool es None si falla la creación

def get_connection():
    if pool:
        try:
            conn = pool.acquire()
            print("Connection acquired from pool.")
            return conn
        except Exception as e:
            print(f"Error acquiring connection from pool: {e}")
            return None
    else:
        print("Pool is not initialized.")
        return None

# Opcional: Función para liberar la conexión de vuelta al pool
def release_connection(conn):
    if pool and conn:
        try:
            pool.release(conn)
            print("Connection released back to pool.")
        except Exception as e:
            print(f"Error releasing connection: {e}")

# Opcional: Función para cerrar el pool al detener la aplicación
def close_pool():
    if pool:
        try:
            pool.close(force=False) # Espera a que las conexiones se liberen
            print("Connection pool closed.")
        except Exception as e:
            print(f"Error closing connection pool: {e}")

# Ejemplo de cómo podrías cerrar el pool al salir (e.g., usando atexit)
atexit.register(close_pool)