from repositories.db import get_connection

class CocheModel:
    def __init__(self, marca, modelo, kilometraje, tipo_combustible, fecha_registro, precio, url, pais, kilometraje_grupo):
        self.marca = marca
        self.modelo = modelo
        self.kilometraje = kilometraje
        self.tipo_combustible = tipo_combustible
        self.fecha_registro = fecha_registro
        self.precio = precio
        self.url = url
        self.pais = pais
        self.kilometraje_grupo = kilometraje_grupo

    @staticmethod
    def obtener_todos():
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM coches")
            columnas = [col[0].lower() for col in cursor.description]
            resultados = [dict(zip(columnas, row)) for row in cursor.fetchall()]
            return resultados
        finally:
            conn.close()

    def insertar_coche(self):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO coches (marca, modelo, kilometraje, tipo_combustible, fecha_registro, precio, url, pais, kilometraje_grupo)
                VALUES (:1, :2, :3, :4, TO_DATE(:5, 'YYYY-MM-DD'), :6, :7, :8, :9)
            """, (
                self.marca,
                self.modelo,
                self.kilometraje,
                self.tipo_combustible,
                self.fecha_registro,
                self.precio,
                self.url,
                self.pais,
                self.kilometraje_grupo
            ))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def insertar_bulk(lista_coches):
        """
        Inserta una lista de objetos CocheModel en la tabla 'coches'.
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO coches (marca, modelo, kilometraje, tipo_combustible, fecha_registro, precio, url, pais, kilometraje_grupo)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)
            """
            data = [
                (
                    coche.marca,
                    coche.modelo,
                    coche.kilometraje,
                    coche.tipo_combustible,
                    coche.fecha_registro,
                    coche.precio,
                    coche.url,
                    coche.pais,
                    coche.kilometraje_grupo
                )
                for coche in lista_coches
            ]
            cursor.executemany(sql, data)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def obtener_por_marca(marca):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM coches WHERE LOWER(marca) = LOWER(:1)", (marca,))
            columnas = [col[0].lower() for col in cursor.description]
            resultados = [dict(zip(columnas, row)) for row in cursor.fetchall()]
            return resultados
        finally:
            conn.close()

    @staticmethod
    def eliminar_por_modelo(modelo):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM coches WHERE modelo = :1", (modelo,))
            conn.commit()
        finally:
            conn.close()
