import time
import pandas as pd
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
                time.sleep(1)
                i+=1

    def save_to_csv(self, filename="listings.csv"):

        #Se guarda lo recuperado del scrapper, no el objeto de la clase.
        self.listing_frame.to_csv(filename, index=False)
        print("Data saved to", filename)

    def quit_browser(self):
        self.browser.quit()
