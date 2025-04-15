import time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By


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
        # self.base_url_de = ("https://www.autoscout24.de/lst/{}/{}/ve_{}?atype=C&cy=D&damaged_listing=exclude&desc=0&"
        #                  "fregfrom={}&fregto={}&powerfrom={}&powerto={}&powertype={}&sort=standard&"
        #                  "source=homepage_search-mask&ustate=N%2CU&zip={}&zipr={}")
        ##url en español y en aleman.
        self.base_url = {
            
            "DE": ("https://www.autoscout24.de/lst/{}/{}/ve_{}?atype=C&cy=D&damaged_listing=exclude&desc=0&"
               "fregfrom={}&fregto={}&powerfrom={}&powerto={}&powertype={}&sort=standard&"
               "source=homepage_search-mask&ustate=N%2CU&zip={}&zipr={}"),
            "ES": ("https://www.autoscout24.es/lst/{}/{}/ve_{}?atype=C&cy=E&damaged_listing=exclude&desc=0&"
               "fregfrom={}&fregto={}&powerfrom={}&powerto={}&powertype={}&sort=standard&"
               "source=homepage_search-mask&ustate=N%2CU&zip={}&zipr={}")
        }
        self.listing_frame = pd.DataFrame(
            columns=["make", "model", "mileage", "fuel-type", "first-registration", "price"])
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--incognito")
        self.options.add_argument("--ignore-certificate-errors")
        self.browser = webdriver.Chrome(options=self.options)

    def generate_urls(self, num_pages, zip):
        """
        Genera una lista de URLs para realizar scraping basándose en el número de páginas y el código postal proporcionados.
        Itera a través de las URLs base y agrega parámetros de paginación para cada página.
        """
        url_list = []
        for base_url in self.base_url.values():
            url_list.append(base_url.format(self.make, self.model, self.version, self.year_from, self.year_to,
                                            self.power_from, self.power_to, self.powertype, zip, self.zipr))
            for i in range(2, num_pages + 1):
                url_to_add = (base_url.format(self.make, self.model, self.version, self.year_from, self.year_to,
                                              self.power_from, self.power_to, self.powertype, zip, self.zipr) +
                              f"&page={i}&sort=standard&source=listpage_pagination&ustate=N%2CU")
                url_list.append(url_to_add)
        return url_list

    def scrape(self, num_pages, verbose=False):
        url_list = []

        #Recorro la lista por key/value
        for ciudad,pais in self.zip_list.items():
            url_list.extend(self.generate_urls(num_pages, ciudad))

        print(url_list)

        for webpage in url_list:
            self.browser.get(webpage)
            listings = self.browser.find_elements("xpath", "//article[contains(@class, 'cldt-summary-full-item')]")
            i=0

            for listing in listings:
                data_make = listing.get_attribute("data-make")
                data_model = listing.get_attribute("data-model")
                data_mileage = listing.get_attribute("data-mileage")
                data_fuel_type = listing.get_attribute("data-fuel-type")
                data_first_registration = listing.get_attribute("data-first-registration")
                data_price = listing.get_attribute("data-price")
                #Hipervínculo al detalle.
                data_url = listing.find_element(By.XPATH, ".//a[@href]").get_attribute("href")

                #Saco el pais según la URL usada.
                if 'https://www.autoscout24.es/' in webpage:
                    data_country = 'ES'
                else:
                    data_country = 'DE'

            
                listing_data = {
                    "make": data_make,
                    "model": data_model,
                    "mileage": data_mileage,
                    "fuel-type": data_fuel_type,
                    "first-registration": data_first_registration,
                    "price": data_price,
                    "url": data_url +' ',
                    "country": data_country
                }
                if verbose:
                    print(listing_data)

                frame = pd.DataFrame(listing_data, index=[0])

                # Guardo en un lsitado lo recuperado del scrapping
                self.listing_frame = self.listing_frame._append(frame, ignore_index=True)

                ##time.sleep(0.3)
                i+=1
            print("****************************************")
            print("Coches scrapeados: "+str(i))
            print("****************************************")
            


    #################################################################
    ## función filter_cars que lea el DataFrame y guarde en otro DataFrame los coches del país "DE" que tengan 
    ## un precio entre un 10% y un 15% más que los del país "ES" 
    ## y con una diferencia de kilometraje de 5,000 arriba o abajo.
    #################################################################



    def filter_cars(self, directory):

        print("Empiezo con el filter_cars")
        ##ADEMÁS DE PROBARLÁ, SI FUNCIONA, FALTARIA GUARDARLA EN CSV#
        es_cars = self.listing_frame[self.listing_frame['country'] == 'ES']
        de_cars = self.listing_frame[self.listing_frame['country'] == 'DE']
        
        filtered_cars = pd.DataFrame(columns=self.listing_frame.columns)

        ##El algoritmo está al revés. Está sacando precios alemanes mas caros que los españoles.
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
                ##matching_de_cars['origen'] = es_car['url']
                matching_de_cars.loc[:, 'origen'] = es_car['url']



            filtered_cars = pd.concat([filtered_cars, matching_de_cars])

        filtered_cars = filtered_cars.drop_duplicates()
        filtered_cars.to_csv(directory, index=False)
        print("Termino con el filter_cars")



    def save_to_csv(self, filename="listings.csv"):

        #Se guarda lo recuperado del scrapper, no el objeto de la clase.
        self.listing_frame.to_csv(filename, index=False)
        print("Data saved to", filename)

    def quit_browser(self):
        self.browser.quit()
