from Miner.AutoScout24Scraper import AutoScout24Scraper
from Analysis.DataProcessor import DataProcessor
from Analysis.MileagePriceRegression import MileagePriceRegression
from Miner.TextFileHandler import TextFileHandler
from models.regiones import RegionDAO
import os
from models.resultado_scrap import CocheModel

class ScrapperBot:
    def __init__(self, make="", model="", version="", year_from="", year_to="",
                 power_from="", power_to="", powertype="kw", num_pages=1, zipr=250):
        self.make = make
        self.model = model
        self.version = version
        self.year_from = year_from
        self.year_to = year_to
        self.power_from = power_from
        self.power_to = power_to
        self.powertype = powertype
        self.num_pages = num_pages  # Should be int or None
        self.zipr = zipr

        self.downloaded_listings_file = f'listings/listings_{self.make}_{self.model}.csv'
        self.output_file_preprocessed = f'listings/listings_{self.make}_{self.model}_preprocessed.csv'
        self.oportunities_file = 'listings/oportunidades.csv'

        # Crear carpeta listings si no existe
        if not os.path.exists("listings"):
            os.makedirs("listings")

    @classmethod
    def run(cls, make="", model="", version="", year_from="", year_to="",
            power_from="", power_to="", powertype="kw", num_pages=1, zipr=250):
        bot = cls(
            make=make,
            model=model,
            version=version,
            year_from=year_from,
            year_to=year_to,
            power_from=power_from,
            power_to=power_to,
            powertype=powertype,
            num_pages=num_pages,
            zipr=zipr
        )
        # Eliminar todos los registros de resultado_scrapp antes de iniciar el scraping
        CocheModel.eliminar_todos()
        # Llamar a get_all_regions sin argumentos
        zip_list = RegionDAO.get_all_regions()

        bot.scrape_autoscout(zip_list)

        """
        Esto está peniente de evaluar y refactorizar, de ver que hace y si es necesario o no.

        data_preprocessed = bot.preprocess()

        """

        # Aquí puedes añadir lógica de análisis adicional

    ## Hay que refactorizar todo esto, hay que ver que me hace falta y que no.
    def preprocess(self):
        processor = DataProcessor(self.downloaded_listings_file)
        data = processor.read_data()
        data_no_duplicates = processor.remove_duplicates(data)
        data_preprocessed = processor.preprocess_data(data_no_duplicates)
        data_rounded = processor.round(data_preprocessed, 1000)
        processor.save_processed_data(data_rounded, self.output_file_preprocessed)

        print("quitando duplicados de oportunidades")
        processorOportunidades = DataProcessor(self.oportunities_file)
        dataOportunidades = processorOportunidades.read_data()
        data_no_duplicates = processorOportunidades.remove_duplicates(dataOportunidades)

        return data_preprocessed

    def scrape_autoscout(self, zip_list):
        scraper = AutoScout24Scraper(self.make, self.model, self.version, self.year_from, self.year_to,
                                     self.power_from, self.power_to, self.powertype, zip_list, self.zipr)
        scraper.scrape(self.num_pages, True)
        #scraper.filter_cars(self.oportunities_file)
        # Esta línea de guardar, hay que matarla y guardar en bbdd
        #scraper.save_to_csv(self.downloaded_listings_file)
        scraper.quit_browser


