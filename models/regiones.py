from typing import List, Dict, Any
import oracledb  # Importar oracledb en lugar de cx_Oracle
from repositories.db import get_connection, release_connection # Importar funciones del pool

class Region:
    def __init__(self, id: int, region: str, capital: str, pais: str):
        self.id = id
        self.region = region
        self.capital = capital
        self.pais = pais

    def __repr__(self):
        return f"Region(id={self.id}, region='{self.region}', capital='{self.capital}', pais='{self.pais}')"

class RegionDAO:
    @staticmethod
    def get_all_regions() -> List[Dict[str, Any]]: # No necesita el parámetro connection, devuelve lista de diccionarios
        query = "SELECT capital, pais FROM regiones"
        result = []
        connection = None  # Inicializar connection a None
        try:
            connection = get_connection() # Obtener conexión del pool
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    # Obtener nombres de columnas para crear diccionarios dinámicamente
                    colnames = [desc[0].lower() for desc in cursor.description]
                    cursor.rowfactory = lambda *args: dict(zip(colnames, args))
                    for row in cursor.fetchall():
                        # Asegurarse de que las claves coincidan con lo esperado ("capital", "pais")
                        # Si los nombres de columna en la BD son diferentes, ajustar aquí o en la consulta
                        result.append({"capital": row.get('capital'), "pais": row.get('pais')})
            else:
                print("Failed to get connection from pool.") # Manejar caso de no obtener conexión
        except oracledb.Error as e:
            print(f"Error executing query: {e}") # Manejar errores de base de datos
        finally:
            if connection:
                release_connection(connection) # Liberar la conexión de vuelta al pool
        return result
