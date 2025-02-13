import pandas as pd


class TextFileHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data_txt(self, encoding='latin-1'):
        try:
            self.df = pd.read_csv(self.file_path, sep=';', encoding=encoding)
        except UnicodeDecodeError:
            print(f"Error: Unable to decode the file with encoding '{encoding}'.")

    def load_data_csv(self):
        self.df = pd.read_csv(self.file_path)

    def export_comune_column(self):
        if self.df is not None:
            comune_column = self.df['Comune'].tolist()
            return comune_column
        else:
            print("Data not loaded. Call load_data() first.")


    """
    Funcion que devuelve un diccionario con la ciudad y el pais
    """
    def export_capoluogo_column(self):
        if self.df is not None:
            
            #Recupero del csv la columna de ciudad y pais
            capoluogo_pais_dict = self.df.set_index(self.df['Capoluogo'].str.lower())['Pais'].to_dict()
            return capoluogo_pais_dict
        else:
            print("Data not loaded. Call load_data() first.")
