import time
from warnings import filters
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from models.resultado_Scrap import CocheModel


class AutoScout24Scraper:
    def __init__(self, make, model, version, year_from, year_to, power_from, power_to, powertype, zip_list, zipr):
        self.make = make
        self.model = model
        self.version = version
        self.year_from = year_from
        self.year_to = year_to
        self.power_from = power_from
        self.power_to = power_to
        self.powertype = powertype
        self.zip_list = zip_list
        self.zipr = zipr
        self.base_url = {
            "DE": ("https://www.autoscout24.de/lst/{}/{}/ve_{}?atype=C&cy=D&damaged_listing=exclude&desc=0&"
                   "fregfrom={}&fregto={}&powerfrom={}&powerto={}&powertype={}&sort=standard&"
                   "source=homepage_search-mask&ustate=N%2CU&zip={}&zipr={}"),
            "ES": ("https://www.autoscout24.es/lst/{}/{}/ve_{}?atype=C&cy=E&damaged_listing=exclude&desc=0&"
                   "fregfrom={}&fregto={}&powerfrom={}&powerto={}&powertype={}&sort=standard&"
                   "source=homepage_search-mask&ustate=N%2CU&zip={}&zipr={}")
        }
        self.listing_frame = pd.DataFrame(
            columns=["make", "model", "mileage", "fuel-type", "first-registration", "price", "url", "country"])
        self.coches = []  # Nueva lista para objetos CocheModel
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--incognito")
        self.options.add_argument("--ignore-certificate-errors")
        self.browser = webdriver.Chrome(options=self.options)

    def generate_urls(self, num_pages, zip_code, country_code):
        """
        Genera una lista de URLs para realizar scraping basándose en el número de páginas, código postal y país proporcionados.
        Selecciona la URL base correcta según el país.
        """
        url_list = []
        base_url = self.base_url.get(country_code.upper())
        if not base_url:
            print(f"Advertencia: Código de país '{country_code}' no encontrado en base_url. No se generarán URLs para {zip_code}.")
            return []

        url_list.append(base_url.format(self.make, self.model, self.version, self.year_from, self.year_to,
                                        self.power_from, self.power_to, self.powertype, zip_code, self.zipr))
        for i in range(2, num_pages + 1):
            url_to_add = (base_url.format(self.make, self.model, self.version, self.year_from, self.year_to,
                                          self.power_from, self.power_to, self.powertype, zip_code, self.zipr) +
                          f"&page={i}&sort=standard&source=listpage_pagination&ustate=N%2CU")
            url_list.append(url_to_add)
        return url_list

    def scrape(self, num_pages, verbose=False):
        url_list = []

        # Iterar sobre la lista de diccionarios
        for region_info in self.zip_list:
            ciudad = region_info.get('capital')  # Obtener la ciudad
            pais = region_info.get('pais')      # Obtener el país

            if ciudad and pais:  # Verificar que ambos valores existen
                url_list.extend(self.generate_urls(num_pages, ciudad, pais))
            else:
                print(f"Advertencia: Información incompleta para la región: {region_info}. Saltando.")

        print(f"Total URLs generadas: {len(url_list)}")

        for webpage in url_list:
            try:
                self.browser.get(webpage)
                time.sleep(1)
            except Exception as e:
                print(f"Error al cargar la página {webpage}: {e}")
                continue

            listings = self.browser.find_elements(By.XPATH, "//article[contains(@class, 'cldt-summary-full-item')]")
            i = 0

            for listing in listings:
                try:
                    data_make = listing.get_attribute("data-make")
                    data_model = listing.get_attribute("data-model")
                    data_mileage = listing.get_attribute("data-mileage")
                    data_fuel_type = listing.get_attribute("data-fuel-type")
                    data_first_registration = listing.get_attribute("data-first-registration")
                    data_price = listing.get_attribute("data-price")
                    data_url_element = listing.find_element(By.XPATH, ".//a[@href]")
                    data_url = data_url_element.get_attribute("href") if data_url_element else None

                    data_country = None
                    for code, url_pattern in self.base_url.items():
                        domain = url_pattern.split('/')[2]
                        if domain in webpage:
                            data_country = code
                            break
                    if not data_country and data_url:
                        if 'autoscout24.es' in data_url:
                            data_country = 'ES'
                        elif 'autoscout24.de' in data_url:
                            data_country = 'DE'

                    listing_data = {
                        "make": data_make,
                        "model": data_model,
                        "mileage": data_mileage,
                        "fuel-type": data_fuel_type,
                        "first-registration": data_first_registration,
                        "price": data_price,
                        "url": data_url + ' ' if data_url else None,
                        "country": data_country
                    }

                    # Crear y añadir objeto CocheModel a la lista
                    coche_obj = CocheModel(
                        marca=data_make,
                        modelo=data_model,
                        kilometraje=data_mileage,
                        tipo_combustible=data_fuel_type,
                        fecha_registro=data_first_registration,
                        precio=data_price,
                        url=data_url,
                        pais=data_country,
                        kilometraje_grupo=None  # O ajusta según lógica necesaria
                    )
                    self.coches.append(coche_obj)

                    if verbose:
                        print(listing_data)

                    frame = pd.DataFrame(listing_data, index=[0])
                    self.listing_frame = pd.concat([self.listing_frame, frame], ignore_index=True)
                    i += 1
                except Exception as e:
                    print(f"Error procesando un listing en {webpage}: {e}")
                    continue

            print("****************************************")
            print(f"Coches scrapeados en {webpage}: {i}")
            print("****************************************")
            time.sleep(1)
        ##Inserto el resultado del scrapping en la base de datos
        CocheModel.insertar_bulk(self.coches)
        

    def filter_cars(self, directory):
        print("Empiezo con el filter_cars")
        es_cars = self.listing_frame[self.listing_frame['country'] == 'ES']
        de_cars = self.listing_frame[self.listing_frame['country'] == 'DE']

        filtered_cars = pd.DataFrame(columns=self.listing_frame.columns)

        for _, es_car in es_cars.iterrows():
            es_price = float(es_car['price'].replace('€', '').replace(',', '').strip())
            es_mileage = int(es_car['mileage'].replace(' km', '').replace(',', '').strip())

            price_min = es_price * 1.05
            price_max = es_price * 1.25

            mileage_min = es_mileage - 10000
            mileage_max = es_mileage + 10000

            matching_de_cars = de_cars[
                (de_cars['price'].apply(lambda x: float(x.replace('€', '').replace(',', '').strip())).between(price_min, price_max)) &
                (de_cars['mileage'].apply(lambda x: int(x.replace(' km', '').replace(',', '').strip())).between(mileage_min, mileage_max))
            ].copy()

            if not matching_de_cars.empty:
                matching_de_cars.loc[:, 'origen'] = es_car['url']

            filtered_cars = pd.concat([filtered_cars, matching_de_cars])

        filtered_cars = filtered_cars.drop_duplicates()
        ##filtered_cars.to_csv(directory, index=False)
        print("Termino con el filter_cars")

    def save_to_csv(self, filename="listings.csv"):
        self.listing_frame.to_csv(filename, index=False)
        print("Data saved to", filename)

    def quit_browser(self):
        self.browser.quit()
