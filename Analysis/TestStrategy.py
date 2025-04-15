#!/usr/bin/env python3

import pandas as pd

# Carga tus datasets


def main():
    print("Empiezo")

    es_cars = archivo[archivo['country'] == 'ES']
    de_cars = archivo[archivo['country'] == 'DE']
    # Para cada coche español, busca coches de_carses con mileage similar y price al menos 30% menor
    resultados = []

    for _, es_car in es_cars.iterrows():  # Renombrar 'rows' a 'es_car' para claridad
        km_min = es_car['mileage'] - 10000
        km_max = es_car['mileage'] + 10000
        # Ajusta el multiplicador para definir "significativamente más barato"
        # Ejemplo: 0.70 para buscar coches al menos un 30% más baratos
        price_max = es_car['price'] * 0.70

        coincidencias = de_cars[
            (de_cars['mileage'] >= km_min) &
            (de_cars['mileage'] <= km_max) &
            (de_cars['price'] <= price_max)
        ]

        # Mover este bloque fuera del if coincidencias.empty
        if not coincidencias.empty:
            # Iterar sobre las coincidencias encontradas
            for _, de_car in coincidencias.iterrows():  # Renombrar 'de_cars' a 'de_car' para evitar conflicto                
                ahorro_porcentaje = round((1 - de_car['price'] / es_car['price']) * 100, 2)  # Calcula el porcentaje de ahorro
                resultados.append({
                    'km_es': es_car['mileage'],
                    'price_es': es_car['price'],
                    'km_de': de_car['mileage'],
                    'price_de': de_car['price'],
                    'ahorro_%': ahorro_porcentaje  # Calcular y añadir el ahorro
                })

    resultados_df = pd.DataFrame(resultados)

    # Mostrar resultados ordenados por ahorro (descomentar y asegurar que la columna existe)
    if not resultados_df.empty and 'ahorro_%' in resultados_df.columns:
        resultados_df.sort_values(by='ahorro_%', ascending=False, inplace=True)
        print(resultados_df.head(10))
    else:
        print("No se encontraron resultados que cumplan los criterios.")


if __name__ == "__main__":
    archivo = pd.read_csv("listings/listings_volkswagen_golf-(alle)_preprocessed.csv")

    main()