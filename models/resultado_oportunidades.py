from repositories.db import get_connection

class AnalisisCocheModel:
    def __init__(self, kilometros_es, precio_es, kilometros_de, precio_de, ahorro_porcentaje, url_es, url_de, marca_es=None, marca_de=None, modelo_es=None, modelo_de=None):
        self.kilometros_es = kilometros_es
        self.precio_es = precio_es
        self.kilometros_de = kilometros_de
        self.precio_de = precio_de
        self.ahorro_porcentaje = ahorro_porcentaje
        self.url_es = url_es
        self.url_de = url_de
        self.marca_es = marca_es
        self.marca_de = marca_de   
        self.modelo_es = modelo_es
        self.modelo_de = modelo_de

    @staticmethod
    def obtener_todos():
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT kilometros_es, precio_es, kilometros_de, precio_de, ahorro_porcentaje, url_es, url_de,
                       marca_es, marca_de, modelo_es, modelo_de
                FROM analisis_coches
            """)
            columnas = [col[0].lower() for col in cursor.description]
            resultados = [dict(zip(columnas, row)) for row in cursor.fetchall()]
            return resultados
        finally:
            conn.close()

    def insertar(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analisis_coches (
                    kilometros_es, precio_es, kilometros_de, precio_de, ahorro_porcentaje, url_es, url_de,
                    marca_es, marca_de, modelo_es, modelo_de
                ) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)
            """, (
                self.kilometros_es,
                self.precio_es,
                self.kilometros_de,
                self.precio_de,
                self.ahorro_porcentaje,
                self.url_es,
                self.url_de,
                self.marca_es,
                self.marca_de,
                self.modelo_es,
                self.modelo_de
            ))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def insertar_bulk(lista_analisis):
        """
        Inserta una lista de objetos AnalisisCocheModel en la tabla 'analisis_coches'.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO analisis_coches (
                    kilometros_es, precio_es, kilometros_de, precio_de, ahorro_porcentaje, url_es, url_de,
                    marca_es, marca_de, modelo_es, modelo_de
                ) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)
            """
            data = [
                (
                    analisis.kilometros_es,
                    analisis.precio_es,
                    analisis.kilometros_de,
                    analisis.precio_de,
                    analisis.ahorro_porcentaje,
                    analisis.url_es,
                    analisis.url_de,
                    analisis.marca_es,
                    analisis.marca_de,
                    analisis.modelo_es,
                    analisis.modelo_de
                )
                for analisis in lista_analisis
            ]
            cursor.executemany(sql, data)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def eliminar_todos():
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM analisis_coches")
            conn.commit()
        finally:
            conn.close()