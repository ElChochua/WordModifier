from pandas import DataFrame
import pandas as pd
from Util import FileManager
class DataProcess:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        match self.file_path.split(".")[-1].lower():
            case "csv":
                return pd.read_csv(self.file_path)
            case "xlsx":
                return pd.read_excel(self.file_path)
            case "json":
                return pd.read_json(self.file_path)
            case "docx":
                fm = FileManager(self.file_path)
                raw_tables = fm.get_all_tables()
                # Converts each table to a DataFrame and returns a list of DataFrames
                tables = [pd.DataFrame([[cell.text for cell in row.cells] for row in table.rows]) for table in raw_tables]
                return tables
            case _:
                raise ValueError("Unsupported file format")