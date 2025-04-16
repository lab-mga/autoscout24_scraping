from Miner.AutoScout24Scraper import AutoScout24Scraper
from Analysis.DataProcessor import DataProcessor
from Analysis.MileagePriceRegression import MileagePriceRegression
from Miner.TextFileHandler import TextFileHandler

import os

##Enfocar más este main como una clase, sobre todo que ahora con flask

def main(scrape=False, analisys=False):
    print('Scrapping ' + str(scrape) + ' analisys ' + str(analisys))
    
   ##Este método no haria, ya lo tengo en bbdd, seria borrar el where_To_search 
    zip_list = where_to_search()
    if scrape:
        scrape_autoscout(zip_list)
        data_preprocessed = preprocess()

    if analisys:
        # Data Processing
        data_preprocessed = preprocess()
        # Mileage-Price Regression





##Sobre esto, sería hacerlo antes de guardar en bbdd¿??, igualmente esto esta raro, habrí que darle una vuelta
def preprocess():
    processor = DataProcessor(downloaded_listings_file)
    data = processor.read_data()
    data_no_duplicates = processor.remove_duplicates(data)
    data_preprocessed = processor.preprocess_data(data_no_duplicates)
    data_rounded = processor.round(data_preprocessed, 1000)
    processor.save_processed_data(data_rounded, output_file_preprocessed)

    ##Ahora vamos con el csv de oportunidades
    print("quitando duplicados de oportunidades")
    processorOportunidades = DataProcessor(oportunities_file)
    dataOportunidades = processorOportunidades.read_data()
    data_no_duplicates = processorOportunidades.remove_duplicates(dataOportunidades)

    return data_preprocessed


def scrape_autoscout(zip_list):
    scraper = AutoScout24Scraper(make, model, version, year_from, year_to, power_from, power_to, powertype, zip_list,
                                 zipr)
    scraper.scrape(num_pages, True)
    scraper.filter_cars(oportunities_file)
    scraper.save_to_csv(downloaded_listings_file)
    scraper.quit_browser()


def where_to_search():
    handler = TextFileHandler(zip_list_file_path)
    handler.load_data_csv()
    zip_list = handler.export_capoluogo_column()
    #zip_list = [item.lower() for item in zip_list
    return zip_list


if __name__ == "__main__":
    make = "volkswagen"
    model = "golf-(alle)"
    version = ""
    year_from = "2018"
    year_to = "2024"
    power_from = ""
    power_to = ""
    powertype = "kw" 
    num_pages = 1
    zipr = 250

    ##Esto seria recupperar de bbdd
    zip_list_file_path = 'Miner/capoluoghi.csv'

    ##esto seía guardar en la bbdd?? No sé si primero en una temporal y luego en una final o como, porque aqui tengo el normal y el preprocesado
    downloaded_listings_file = f'listings/listings_{make}_{model}.csv'
    output_file_preprocessed = f'listings/listings_{make}_{model}_preprocessed.csv'
    ##############################

    ##Esto seria guardarlo igual en tabla, aunq tengo el TestSTrategy que hace algo parecido pero distinto, habría que vuer cual me renta mas
    oportunities_file = 'listings/oportunidades.csv'

    # Create the "listings" folder if it doesn't exist
    #Esto ya no haria falta si voy por bbdd
    if not os.path.exists("listings"):
        os.makedirs("listings")

    # Run the main function    
    main(scrape=True, analisys=False)
    print('finished')
