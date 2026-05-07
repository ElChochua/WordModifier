import tkinter as tk
from tkinter import PhotoImage
from tkinter import Spinbox
from CTkMessagebox import CTkMessagebox
import customtkinter
from Util.DataProcess import DataProcess
from Util.TableSelector import TableSelector
from os import path
from customtkinter import filedialog
import customtkinter as ctt
import pandas as pd
from PIL import Image
class MyApp:
    assets_path = path.abspath(path.join(path.dirname(__file__),'..', "assets"))
    markers = []
    data = {}
    def __init__(self, root):
        self.root = root
        self.root.title("DockGen")
        #Default Size and position
        self.root.geometry('820x600+300+300')
        self.root.resizable(True,True)
        self.root._set_appearance_mode("light") #default
        self.doc_path = None
        self.data_path = None
        self.root.grid_columnconfigure(0, weight=0, minsize=290) 
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.data =  []

        # Header frame
        self.header_frame = ctt.CTkFrame(master=self.root)
        
        # Left frame
        self.left_frame = ctt.CTkFrame(master=self.root)
        
        # Template section frame
        self.template_section_frame = ctt.CTkFrame(master=self.left_frame )
        
        # Markers frame
        self.markers_section_frame = ctt.CTkFrame(master=self.left_frame )
        self.markers_frame = ctt.CTkScrollableFrame(master=self.markers_section_frame )
        
        # Data Frame
        self.data_frame = ctt.CTkFrame(master=self.left_frame )
        # Record control frame
        self.records_section_frame = ctt.CTkFrame(master=self.root )
        self.record_controll_frame = ctt.CTkFrame(master=self.records_section_frame )
        self.records_frame = ctt.CTkScrollableFrame(master=self.records_section_frame )
        self.records_section_frame.columnconfigure(0, weight=1)
        self.records_section_frame.rowconfigure(1, weight=1)
        self.create_widgets()

    def create_widgets(self):
        #header
        header_label = ctt.CTkLabel(master=self.header_frame, text="DocGen", font=ctt.CTkFont(size=24, weight="bold"))
        unlock_doc_button = ctt.CTkButton(master=self.header_frame, text="Unlock Doc", command=lambda: CTkMessagebox(title="Error", message="No se ha seleccionado un archivo de plantilla.", icon="cancel", option_1="OK"))   
        #header full width
        self.header_frame.grid_columnconfigure(0, weight=1) 
        self.header_frame.grid_columnconfigure(1, weight=1)
        #label full on left and button full on right and the center a big gap between them responsive to the window size
        header_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        unlock_doc_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        self.header_frame.grid(row=0,column=0, sticky="ew", columnspan=2)
        
        #left frame
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(1, weight=0)
        self.left_frame.grid_rowconfigure(0, weight=0)
        self.left_frame.grid_rowconfigure(1, weight=0)
        self.left_frame.grid_rowconfigure(2, weight=0)
        self.left_frame.grid(row=1, column=0, sticky="nsew")
        
        #template section 
        select_file_button = ctt.CTkButton(master=self.template_section_frame, text="Select Doc", command=self.select_template)
        select_file_label = ctt.CTkLabel(master=self.template_section_frame, text="Template")


        select_file_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        select_file_button.grid(row=1, column=0, padx=5, pady=5)
        self.template_section_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        #markers section
        markers_label = ctt.CTkLabel(master=self.markers_section_frame, text="Markers")
        markers_entry = ctt.CTkEntry(master=self.markers_section_frame)
        markers_entry.bind("<Return>", lambda event: self.on_marker_entry(event))
        rotate_icon = ctt.CTkImage(light_image=Image.open(path.join(self.assets_path, "rotate_icon.png")),
                                    dark_image=Image.open(path.join(self.assets_path, "rotate_icon.png")), size=(20, 20))
        remove_all_markers_button = ctt.CTkButton(master=self.markers_section_frame,text="", command=self.remove_all_markers, image=rotate_icon, 
                                                    width=rotate_icon.cget("size")[0], height=rotate_icon.cget("size")[1], bg_color="transparent", fg_color="transparent")
        '''When you add a new marker, a button will be created with the marker's name. When you click the button, it will be removed and the data associated with that marker will be deleted.'''
        markers_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        remove_all_markers_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")
        markers_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.markers_section_frame.grid_columnconfigure(0, weight=1)
        self.markers_section_frame.grid_columnconfigure(1, weight=0)
        self.markers_frame.grid_columnconfigure(0, weight=1)
        self.markers_frame.grid_columnconfigure(1, weight=1)
        self.markers_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.markers_section_frame.grid(row=1, column=0, padx=5, sticky="ew")

        #data section
        data_icon = ctt.CTkImage(light_image=Image.open(path.join(self.assets_path, "data_icon_white.png")), dark_image=Image.open(path.join(self.assets_path, "data_icon_black.png")), size=(20, 20))
        no_data_icon = ctt.CTkImage(light_image=Image.open(path.join(self.assets_path, "no_data_white.png")), dark_image=Image.open(path.join(self.assets_path, "no_data_black.png")), size=(20, 20))
        data_import_label = ctt.CTkLabel(master=self.data_frame, text="Data")
        data_import_button = ctt.CTkButton(master=self.data_frame, text="Import Data",image=data_icon, compound="left", command=self.import_data)
        manual_data_button = ctt.CTkButton(master=self.data_frame, text="Add Data Manually", image=no_data_icon, compound="left", command=self.add_record_manually)
        '''when you click the "Add Data Manually" button, it will open a new window with a table. The table will have two columns: "Marker" and "Value". You can add as many rows as you want. When you click the "Save" button, it will save the data in a dictionary. The key of the dictionary will be the marker and the value of the dictionary will be the value you provided.'''
        data_import_label.grid(row=0, column=0)
        data_import_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        manual_data_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.data_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        #record control section
        '''records section will have a header with the count of records, a button to delete all of them, a button to delete the selected one
        the records will be displayed in a listbox with a scrollbar, on top of the listbox there will be the markers associated with the record, and the data associated with the record. When you click on a record, it will show the markers and data associated with that record.'''
        #records section

        records_label = ctt.CTkLabel(master=self.records_section_frame, text="Records", font=ctt.CTkFont(size=16, weight="bold"))
        delete_all_records_button = ctt.CTkButton(master=self.records_section_frame, text="Delete All Records")
        delete_all_records_button = ctt.CTkButton(master=self.records_section_frame, text="Clear All", command=self.remove_all_records)
        delete_selected_record_button = ctt.CTkButton(master=self.records_section_frame, text="Delete Selected Record", command=self.remove_selected_records)

        delete_all_records_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")
        delete_selected_record_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        records_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")


        self.records_section_frame.grid(row=1, column=1, sticky="nsew")
        #records section
        #horizontal_scroll = ctt.CTkScrollbar(master=self.records_frame, orientation="horizontal")
        #horizontal_scroll.grid(row=1, column=0, sticky="ew")
        self.records_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")



    def add_marker(self, marker):
        if marker in self.markers:
            CTkMessagebox(title="Error", message="Marker already exists", icon="cancel")
            return
        elif marker.strip() == "":
            CTkMessagebox(title="Error", message="Marker cannot be empty", icon="cancel")
            return
        self.markers.append(marker)
        self.data[marker] = "" #add the marker as a column in the data with empty values
        #create button with marker name
        if len(self.markers) > 0:
            self.update_markers_grid()
            if marker not in self.data:
                self.data[marker] = ""

    def update_markers_grid(self):
        for widget in self.markers_frame.winfo_children():
            if isinstance(widget, ctt.CTkButton):
                widget.destroy()

        for index, marker in enumerate(self.markers):
            r = index // 2
            c = index % 2
            print(f"Adding marker '{marker}' at row {r}, column {c}")
            btn = ctt.CTkButton(master=self.markers_frame, text=marker, command=lambda m=marker: self.remove_marker(m))
            btn.grid(row=r, column=c, padx=5, pady=5, sticky="ew")

    def remove_marker(self, marker):
        if marker in self.markers:
            self.markers.remove(marker)
            #remove column from the data
            #self.data.pop(marker)
            self.data.drop(columns=marker, inplace=True)        
            print(f"Number of markers remaining: \n{(self.data)}")
            #remove button with marker name

            for widget in self.markers_section_frame.grid_slaves():
                if isinstance(widget, ctt.CTkButton) and widget.cget("text") == marker:
                    widget.destroy()
                    break
            self.update_markers_grid()
            self.update_record_table()
            #remove data associated with the marker
            if marker in self.data:
                del self.data[marker]

    def remove_all_markers(self):
        for marker in self.markers[:]:
            self.remove_marker(marker)

    def on_marker_entry(self, event):
        marker = event.widget.get()
        self.add_marker(marker)
        self.data[marker] = ""
        self.update_record_table()
        print(f"Number of markers: {(self.markers)}")
        event.widget.delete(0, tk.END)

    def add_record(self):
        #add the records as a table with the markers as columns and the data as values, each record will be a new row in the table from the data imported, if the data is a list of dictionaries, each dictionary will be a new record, if the data is a dictionary, it will be a single record
        if isinstance(self.data, list):
            for record in self.data:
                if isinstance(record, dict):
                    self.create_record(record)
        elif isinstance(self.data, dict):
            self.create_record(self.data)
    def create_record(self, record):
        record_frame = ctt.CTkFrame(master=self.records_frame)
        for index, marker in enumerate(self.markers):
            value = record.get(marker, "")
            marker_label = ctt.CTkLabel(master=record_frame, text=f"{marker}: {value}")
            marker_label.grid(row=0, column=index, padx=5, pady=5, sticky="w")
        record_frame.pack(fill="x", padx=5, pady=5)
    def update_record_table(self):
            for widget in self.records_frame.winfo_children():
                widget.destroy()

            if self.data is None or self.data.empty:
                return

            self.records_frame.configure(fg_color=("gray75", "gray30"))

            columns = ["Sel"] + [str(marker) for marker in self.markers]
            
            for j, col_name in enumerate(columns):
                header_lbl = ctt.CTkLabel(
                    master=self.records_frame, 
                    text=col_name.upper(), 
                    font=ctt.CTkFont(weight="bold", size=13),
                    fg_color=("gray60", "gray20"), 
                    text_color=("black", "white"),
                    corner_radius=0,
                    height=35
                )
                header_lbl.grid(row=0, column=j, sticky="nsew", padx=1, pady=1)
                

                if j == 0:
                    self.records_frame.grid_columnconfigure(j, weight=0, minsize=40) # Columna de Checkbox pequeña
                else:
                    self.records_frame.grid_columnconfigure(j, weight=1, uniform="columnas_datos")

            self.check_vars = [] 

            for i, (index, row) in enumerate(self.data.iterrows()):
                actual_row = i + 1
                
                if i % 2 == 0:
                    row_color = ("#F9F9F9", "#2B2B2B")
                else:
                    row_color = ("#EFEFEF", "#212121")
                
                var = ctt.BooleanVar()
                self.check_vars.append((index, var))
                
                cb_frame = ctt.CTkFrame(master=self.records_frame, fg_color=row_color, corner_radius=0)
                cb_frame.grid(row=actual_row, column=0, sticky="nsew", padx=1, pady=1)
                
                cb = ctt.CTkCheckBox(master=cb_frame, text="", variable=var, width=20)
                cb.pack(pady=5, padx=10)

                for j, value in enumerate(row):
                    raw_text = "" if pd.isna(value) else str(value).replace("\n", " ")
                    
                    display_text = raw_text[:45] + "..." if len(raw_text) > 45 else raw_text

                    data_cell = ctt.CTkEntry(
                        master=self.records_frame, 
                        fg_color=row_color,
                        text_color=("black", "white"),
                        corner_radius=0,
                        height=30
                    )
                    data_cell.insert(0, display_text)
                    data_cell.bind("<Return>", lambda event, r=index, c=self.data.columns[j]: self.edit_cell(event, r, c))
                    data_cell.grid(row=actual_row, column=j+1, sticky="nsew", padx=1, pady=1)         

    def edit_cell(self, event, row_index, column_name):
        new_value = event.widget.get().strip()
        original_value = self.data.at[row_index, column_name]

        col_dtype = self.data[column_name].dtype

        try:
            if new_value == "":
                self.data.at[row_index, column_name] = pd.NA
                
            elif pd.api.types.is_integer_dtype(col_dtype):
                self.data.at[row_index, column_name] = int(new_value)
                
            elif pd.api.types.is_float_dtype(col_dtype):
                self.data.at[row_index, column_name] = float(new_value)
                
            else:
                self.data.at[row_index, column_name] = new_value

        except ValueError:
            CTkMessagebox(title="Error", message=f"Invalid Value Type. Expected {col_dtype}.", icon="cancel", option_1="OK")
            
            event.widget.delete(0, tk.END)
            safe_val = "" if pd.isna(original_value) else str(original_value)
            event.widget.insert(0, safe_val)
            return

        print(f"Updated cell at row {row_index}, column '{column_name}' to '{new_value}'")
        # print(self.data) # Opcional: comentar para no saturar la consola
        self.update_record_table()


    def select_template(self):
        file = filedialog.askopenfilename(title="Select Template", filetypes=[("Word Documents", "*.docx")])
        if file:
            self.doc_path = file
            template_name_entry = ctt.CTkEntry(master=self.template_section_frame)
            template_name_entry.insert(0, f"{path.basename(file)}")
            #filename readonly
            template_name_entry.configure(state="readonly")
            template_name_entry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
            print(f"Selected template: {self.doc_path}")

    def import_data(self):
            data_file = filedialog.askopenfilename(title="Select Data File", filetypes=[("Data Files", ("*.csv", "*.xlsx", "*.json", "*.docx")), ("All Files", "*.*")])
            
            if not data_file:
                return 
    
            self.data_path = data_file
            ext = data_file.split(".")[-1].lower()
            if ext == "xlsx":
                input_dialog = customtkinter.CTkInputDialog(title="Select Table", text="Excel File Detected. Please enter the row number of the table you want to use:")
                row_input = input_dialog.get_input()
                if row_input is None: return 
                
                try:
                    table_number = int(row_input)
                    data = DataProcess.read_data(data_file, skiprows=table_number-1)
                    
                    self.data = data.loc[:, ~data.columns.astype(str).str.contains("^Unnamed")]
                    
                except ValueError:
                    CTkMessagebox(title="Error", message="Invalid table number. Please enter a valid integer.", icon="cancel", option_1="OK")
                    return
                
            elif ext == "docx":
                raw_data = DataProcess.read_data(data_file)
                
                if len(raw_data) > 1:
                    selector = TableSelector(self.root, raw_data)
                    self.root.wait_window(selector)
                    target_index = selector.selected_index
                    
                    if target_index is None: 
                        return 
                        
                    self.data = raw_data[target_index]
                    
                elif len(raw_data) == 1:
                    self.data = raw_data[0]
                else:
                    self.data = []
                if len(self.data) > 0:
                    self.markers = list(self.data.columns)
                    self.update_markers_grid()
            else:
                self.data = DataProcess.read_data(data_file)
                self.markers = list(self.data.columns)
                self.update_markers_grid()
            if self.data is None or len(self.data) <= 0:
                CTkMessagebox(title="Error", message="Failed to read data from the file. This may be due to an unsupported file format or cannot read any data.", icon="cancel", option_1="OK")
                return
            if len(self.data) > 0:
                self.data.columns = [str(col).strip().replace(" ", "_") for col in self.data.columns]
                self.markers = list(self.data.columns)
                self.update_markers_grid()

            self.update_record_table()
            #remove empty columns button
            remove_empty_columns_button = ctt.CTkButton(master=self.data_frame, text="Remove Empty Columns", command=self.remove_empty_columns)
            remove_empty_columns_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")
            
            # Mostramos el nombre del archivo en la UI
            data_name_entry = ctt.CTkEntry(master=self.data_frame)
            data_name_entry.insert(0, f"{path.basename(data_file)}")
            data_name_entry.configure(state="readonly")
            data_name_entry.grid(row=1, column=1, sticky="ew")
    def remove_empty_columns(self):
        if self.data is not None and not self.data.empty:
            #replace the empty values with nan
            self.data.replace("", pd.NA, inplace=True)
            self.data.dropna( how='all', inplace=True)    
            self.data.dropna(axis=1, how='all', inplace=True)
            self.markers = list(self.data.columns)
            self.update_markers_grid()
            self.update_record_table()
    def remove_all_records(self):
        self.data = pd.DataFrame() 
        self.update_record_table()
    
    def add_record_manually(self):
        #open a new window with a table to add the data manually, the table will have two columns: "Marker" and "Value", and a button to save the data, when you click the button, it will save the data in a dictionary, the key of the dictionary will be the marker and the value of the dictionary will be the value you provided
        manual_data_window = ctt.CTkToplevel(self.root)
        manual_data_window.title("Add Data Manually")
        manual_data_window.geometry("400x300")
        manual_data_window.grid_columnconfigure(0, weight=1)
        manual_data_window.grid_rowconfigure(0, weight=1)
        table_frame = ctt.CTkScrollableFrame(manual_data_window)
        table_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_columnconfigure(1, weight=1)
        table_frame.grid_rowconfigure(0, weight=0)
        marker_label = ctt.CTkLabel(table_frame, text="Marker", font=ctt.CTkFont(weight="bold"))
        value_label = ctt.CTkLabel(table_frame, text="Value", font=ctt.CTkFont(weight="bold"))
        marker_label.grid(row=0, column=0, padx=5, pady=5)
        value_label.grid(row=0, column=1, padx=5, pady=5)
        entries = []
        for i, marker in enumerate(self.markers):
            marker_lbl = ctt.CTkLabel(table_frame, text=marker)
            marker_lbl.grid(row=i+1, column=0, padx=5, pady=5)
            value_entry = ctt.CTkEntry(table_frame)
            value_entry.grid(row=i+1, column=1, padx=5, pady=5)
            entries.append((marker, value_entry))

        def save_manual_data():
            #insert the new values into the data
            new_record_df = pd.DataFrame(columns=self.markers)
            for marker, entry in entries:
                value = entry.get()
                new_record_df.at[0, marker] = value

            self.data = pd.concat([self.data, new_record_df], ignore_index=True)
            self.update_record_table()
            manual_data_window.destroy()
        save_button = ctt.CTkButton(manual_data_window, text="Save", command=save_manual_data)
        save_button.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.update_record_table()
    def remove_selected_records(self):
        selected_indices = [index for index, var in self.check_vars if var.get()]
        if not selected_indices:
            CTkMessagebox(title="Error", message="No records selected. Please select at least one record to delete.", icon="cancel", option_1="OK")
            return
        print(f"Selected indices for deletion: {selected_indices}")
        confirm = CTkMessagebox(title="Confirm Deletion", message=f"Are you sure you want to delete {len(selected_indices)} selected record(s)?", icon="warning", option_2="No", option_1="Yes")
        if confirm.get() == "Yes":
            self.data.drop(index=selected_indices, inplace=True)
            self.data.reset_index(drop=True, inplace=True)
            self.update_record_table()