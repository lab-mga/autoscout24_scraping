#!/usr/bin/env python3

import pandas as pd
from models.resultado_scrap import CocheModel
from models.resultado_oportunidades import AnalisisCocheModel


class OportunidadesAnalyzer:
    @classmethod
    def analizar_oportunidades(cls, target_price):
        # Obtener datos desde la base de datos usando CocheModel
        print("Empiezo el análisis de oportunidades")
        coches = CocheModel.obtener_todos()
        if not coches:
            return  # No hace nada si no hay datos

        archivo = pd.DataFrame(coches)
        es_cars = archivo[archivo['pais'] == 'ES']
        de_cars = archivo[archivo['pais'] == 'DE']
        resultados = []

        for _, es_car in es_cars.iterrows():
            km_min = es_car['kilometraje'] - 10000
            km_max = es_car['kilometraje'] + 10000

            # Calcular el precio máximo permitido en DE, target price es el porcentaje de ahorro,
            #Si quiero un 20% de ahorro, el param recibe un 20, y el precio máximo es el 80% del precio en ES
            price_max = es_car['precio'] * (100 - (target_price/100))

            # Filtrar por misma marca y modelo además de los criterios existentes
            coincidencias = de_cars[
                (de_cars['kilometraje'] >= km_min) &
                (de_cars['kilometraje'] <= km_max) &
                (de_cars['precio'] <= price_max) &
                (de_cars['marca'] == es_car['marca']) &
                (de_cars['modelo'] == es_car['modelo']) &
                (de_cars['caballos'] == es_car['caballos']) 
            ]

            if not coincidencias.empty:
                for _, de_car in coincidencias.iterrows():
                    ahorro_porcentaje = round((1 - de_car['precio'] / es_car['precio']) * 100, 2)
                    resultados.append(
                        AnalisisCocheModel(
                            kilometros_es=es_car['kilometraje'],
                            precio_es=es_car['precio'],
                            kilometros_de=de_car['kilometraje'],
                            precio_de=de_car['precio'],
                            ahorro_porcentaje=ahorro_porcentaje,
                            url_es=es_car.get('url', ''),  # Asume que existe la columna 'url' para ES
                            url_de=de_car.get('url', ''),  # Asume que existe la columna 'url' para DE
                            marca_es=es_car.get('marca', ''),
                            marca_de=de_car.get('marca', ''),
                            modelo_es=es_car.get('modelo', ''),
                            modelo_de=de_car.get('modelo', '')
                        )
                    )

        print("Acabo el análisis, inserto en bulk")

        if resultados:
            AnalisisCocheModel.insertar_bulk(resultados)
        # No retorna nada
        print("Acabo de insertar en bulk")


if __name__ == "__main__":
    OportunidadesAnalyzer.analizar_oportunidades()
    print("Análisis completado e insertado en la base de datos.")