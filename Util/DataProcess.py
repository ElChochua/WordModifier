import pandas as pd
from Util import FileManager
import docx2txt
import re
class DataProcess:
    def __init__(self, file_path):
        self.file_path = file_path
    @staticmethod
    def get_data(file_path, **kwargs):
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
                dataframes = []
                if markers := kwargs.get("from_markers"):
                    text = docx2txt.process(file_path)
                    
                    escaped_markers = [re.escape(m) for m in markers]
                    patron_parada_conocidos = "|".join(escaped_markers)
                    
                    generic_stop_pattern = r"(?:\n|\t|\s{3,})[A-Za-zÁÉÍÓÚÑáéíóúñ][A-Za-zÁÉÍÓÚÑáéíóúñ\s]{0,25}:"
                    
                    total_stop_pattern = f"({patron_parada_conocidos}|{generic_stop_pattern})"
                    
                    document_data = {}
                    for marker in markers:
                        regex = rf"{re.escape(marker)}(.*?)(?={total_stop_pattern}|$)"
                        
                        match = re.search(regex, text, re.DOTALL)
                        
                        if match:
                            cleaned_match = match.group(1).replace("\n", " ").replace("\t", " ").strip()
                            document_data[marker] = cleaned_match
                        else:
                            document_data[marker] = None                            
                            
                    if document_data:
                        df = pd.DataFrame([document_data])
                        dataframes.append(df)
                        
                else:
                    fm = FileManager(file_path)
                    raw_tables = fm.get_all_tables()
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
                print(dataframes)
                return dataframes
            case _:
                raise ValueError("Unsupported file format")