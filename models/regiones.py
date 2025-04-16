from typing import List
import cx_Oracle

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
    def get_all_regions(connection: cx_Oracle.Connection) -> List[Region]:
        query = "SELECT id, region, capital, pais FROM regiones"
        regions = []
        with connection.cursor() as cursor:
            cursor.execute(query)
            for row in cursor.fetchall():
                regions.append(Region(id=row[0], region=row[1], capital=row[2], pais=row[3]))
        return regions
