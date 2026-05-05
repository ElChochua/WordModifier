from pandas import DataFrame
import pandas as pd
from Util import FileManager
class DataProcess:
    def __init__(self, file_path):
        self.file_path = file_path
    @staticmethod
    def read_data(file_path, **kwargs):
        match file_path.split(".")[-1].lower():
            case "csv":
                return pd.read_csv(file_path, **kwargs)
            case "xlsx":
                return pd.read_excel(file_path, **kwargs)
            case "json":
                return pd.read_json(file_path)
            case "sav":
                return pd.read_spss(file_path)
            case "docx":
                fm = FileManager(file_path)
                raw_tables = fm.get_all_tables()
                dataframes = []
                for table in raw_tables:
                    #convert table to list of lists
                    table_data = [[cell.text.strip() for cell in row.cells] for row in table.rows]
                    
                    if len(table_data) > 1:
                        # if the table has more than 1 row, we assume the first row is the header
                        headers = table_data[0]
                        # the rest of the rows are the data
                        rows = table_data[1:]
                        
                        # create a DataFrame from the rows and headers
                        df = pd.DataFrame(rows, columns=headers)
                        dataframes.append(df)
                    elif len(table_data) == 1:
                        # if the table has only 1 row, we create a DataFrame with that row as the header and no data
                        df = pd.DataFrame(columns=table_data[0])
                        dataframes.append(df)

                return dataframes
            case _:
                raise ValueError("Unsupported file format")