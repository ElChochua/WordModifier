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
from tksheet import Sheet
from Util.LanguageManager import LanguageManager
from Util.FileManager import FileManager

class MyApp:
    assets_path = path.abspath(path.join(path.dirname(__file__),'..', "assets"))
    markers = []
    data: pd.DataFrame = pd.DataFrame()
    def __init__(self, root):
        self.root = root
        self.root.title("DockGen")
        #Default Size and position
        self.root.geometry('820x600+300+300')
        self.root.resizable(True,True)
        self.root._set_appearance_mode("light") #default
        self.doc_path = None
        self.root.grid_columnconfigure(0, weight=0, minsize=290) 
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.markers = []
        self.data = pd.DataFrame()
        self.records_sheet = None
        self.lang = LanguageManager()
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
        self.extract_from_markers_checkbox = ctt.CTkCheckBox(master=self.data_frame, text="", command=lambda: ())

        # Record control frame
        self.records_section_frame = ctt.CTkFrame(master=self.root )
        self.record_controll_frame = ctt.CTkFrame(master=self.records_section_frame )
        self.records_frame = ctt.CTkFrame(master=self.records_section_frame )
        self.records_section_frame.columnconfigure(0, weight=1)
        self.records_section_frame.rowconfigure(1, weight=1)
        self.create_widgets()

    def create_widgets(self):
        #header
        header_label = ctt.CTkLabel(master=self.header_frame, text="DocGen", font=ctt.CTkFont(size=24, weight="bold"))
        unlock_doc_button = ctt.CTkButton(master=self.header_frame, text=self.lang.get("unlock_document"), command=lambda: CTkMessagebox(title=self.lang.get("error"), message=self.lang.get("no_template_selected"), icon="cancel", option_1=self.lang.get("ok")))   
        generate_docs_button = ctt.CTkButton(master=self.header_frame, text=self.lang.get("generate_documents"), command=self.generate_documents)
        #header full width
        self.header_frame.grid_columnconfigure(0, weight=1) 
        self.header_frame.grid_columnconfigure(1, weight=1)
        #label full on left and button full on right and the center a big gap between them responsive to the window size
        header_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        unlock_doc_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")
        generate_docs_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")
        self.header_frame.grid(row=0,column=0, sticky="ew", columnspan=2)
        
        #left frame
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(1, weight=0)
        self.left_frame.grid_rowconfigure(0, weight=0)
        self.left_frame.grid_rowconfigure(1, weight=0)
        self.left_frame.grid_rowconfigure(2, weight=0)
        self.left_frame.grid(row=1, column=0, sticky="nsew")
        
        #template section 
        select_file_button = ctt.CTkButton(master=self.template_section_frame, text=self.lang.get("select_template"), command=self.select_template)
        select_file_label = ctt.CTkLabel(master=self.template_section_frame, text=self.lang.get("template"))
        select_output_button = ctt.CTkButton(master=self.template_section_frame, text=self.lang.get("select_output_folder"), command=self.select_output)
        select_output_label = ctt.CTkLabel(master=self.template_section_frame, text=self.lang.get("output_folder"))


        select_file_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        select_file_button.grid(row=1, column=0, padx=5, pady=5)
        select_output_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        select_output_button.grid(row=1, column=1, padx=5, pady=5)
        self.template_section_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        #markers section
        markers_label = ctt.CTkLabel(master=self.markers_section_frame, text=self.lang.get("markers"))
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
        data_import_label = ctt.CTkLabel(master=self.data_frame, text=self.lang.get("data"))
        data_import_button = ctt.CTkButton(master=self.data_frame, text=self.lang.get("import_data"), image=data_icon, compound="left", command=self.import_data)
        manual_data_button = ctt.CTkButton(master=self.data_frame, text=self.lang.get("add_data_manually"), image=no_data_icon, compound="left", command=self.add_record_manually)
        extract_from_markers_label = ctt.CTkLabel(master=self.data_frame, text=self.lang.get("extract_from_markers"))
        '''when you click the "Add Data Manually" button, it will open a new window with a table. The table will have two columns: "Marker" and "Value". You can add as many rows as you want. When you click the "Save" button, it will save the data in a dictionary. The key of the dictionary will be the marker and the value of the dictionary will be the value you provided.'''
        data_import_label.grid(row=0, column=0)
        data_import_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        manual_data_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        extract_from_markers_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.extract_from_markers_checkbox.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.data_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        #record control section
        '''records section will have a header with the count of records, a button to delete all of them, a button to delete the selected one
        the records will be displayed in a listbox with a scrollbar, on top of the listbox there will be the markers associated with the record, and the data associated with the record. When you click on a record, it will show the markers and data associated with that record.'''
        #records section

        records_label = ctt.CTkLabel(master=self.records_section_frame, text=self.lang.get("records"), font=ctt.CTkFont(size=16, weight="bold"))
        delete_all_records_button = ctt.CTkButton(master=self.records_section_frame, text=self.lang.get("delete_all_records"))
        delete_all_records_button = ctt.CTkButton(master=self.records_section_frame, text=self.lang.get("clear_all"), command=self.remove_all_records)
        remove_empty_rows_button = ctt.CTkButton(master=self.records_section_frame, text=self.lang.get("remove_empty_rows"), command=self.remove_empty_rows)
        delete_all_records_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")
        remove_empty_rows_button.grid(row=0, column=3, padx=5, pady=5, sticky="e")
        records_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")


        self.records_section_frame.grid(row=1, column=1, sticky="nsew")
        #records section
        #horizontal_scroll = ctt.CTkScrollbar(master=self.records_frame, orientation="horizontal")
        #horizontal_scroll.grid(row=1, column=0, sticky="ew")
        self.records_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")

    def _sheet_theme_kwargs(self):
        return {
            "frame_bg": "#E5E5E5",
            "table_bg": "#F8F8F8",
            "table_fg": "#1F1F1F",
            "table_grid_fg": "#D0D0D0",
            "header_bg": "#D9D9D9",
            "header_fg": "#1F1F1F",
            "header_grid_fg": "#C4C4C4",
            "index_bg": "#D9D9D9",
            "index_fg": "#1F1F1F",
            "index_grid_fg": "#C4C4C4",
            "popup_menu_bg": "#F2F2F2",
            "popup_menu_fg": "#1F1F1F",
            "popup_menu_highlight_bg": "#CFCFCF",
            "popup_menu_highlight_fg": "#1F1F1F",
            "table_selected_cells_bg": "#CFE0F5",
            "table_selected_cells_fg": "#1F1F1F",
            "table_selected_cells_border_fg": "#7FA7D8",
            "table_selected_rows_bg": "#DDEAF8",
            "table_selected_rows_fg": "#1F1F1F",
            "table_selected_rows_border_fg": "#7FA7D8",
            "table_selected_columns_bg": "#DDEAF8",
            "table_selected_columns_fg": "#1F1F1F",
            "table_selected_columns_border_fg": "#7FA7D8",
            "index_selected_rows_bg": "#DDEAF8",
            "index_selected_rows_fg": "#1F1F1F",
            "header_selected_columns_bg": "#7FA7D8",
            "header_selected_columns_fg": "#FFFFFF",
            "header_selected_cells_bg": "#CFE0F5",
            "header_selected_cells_fg": "#1F1F1F",
            "index_selected_cells_bg": "#CFE0F5",
            "index_selected_cells_fg": "#1F1F1F",
            "vertical_scroll_background": "#E5E5E5",
            "horizontal_scroll_background": "#E5E5E5",
            "vertical_scroll_troughcolor": "#F2F2F2",
            "horizontal_scroll_troughcolor": "#F2F2F2",
            "vertical_scroll_lightcolor": "#FFFFFF",
            "horizontal_scroll_lightcolor": "#FFFFFF",
            "vertical_scroll_darkcolor": "#A9A9A9",
            "horizontal_scroll_darkcolor": "#A9A9A9",
            "vertical_scroll_active_bg": "#BFBFBF",
            "horizontal_scroll_active_bg": "#BFBFBF",
            "vertical_scroll_not_active_bg": "#D0D0D0",
            "horizontal_scroll_not_active_bg": "#D0D0D0",
            "vertical_scroll_pressed_bg": "#B0B0B0",
            "horizontal_scroll_pressed_bg": "#B0B0B0",
            "outline_color": "#9A9A9A",
            "drag_and_drop_bg": "#7FA7D8",
            "resizing_line_fg": "#4A4A4A",
        }


    def extract_checkbox_changed(self):
        return self.extract_from_markers_checkbox.get()        
    def add_marker(self, marker):
        if marker in self.markers:
            CTkMessagebox(title="Error", message=self.lang.get("markers_exist").format(marker=marker), icon="cancel")
            return
        elif marker.strip() == "":
            CTkMessagebox(title="Error", message=self.lang.get("marker_cannot_be_empty"), icon="cancel")
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
            if marker in self.data.columns:
                self.data.drop(columns=marker, inplace=True)
            print(f"Number of markers remaining: \n{(self.data)}")
            #remove button with marker name

            for widget in self.markers_section_frame.grid_slaves():
                if isinstance(widget, ctt.CTkButton) and widget.cget("text") == marker:
                    widget.destroy()
                    break
            self.update_markers_grid()
            self.update_record_table()

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

    def _coerce_sheet_value(self, column_name, value):
        if value is None:
            return pd.NA

        if isinstance(value, str):
            value = value.strip()

        if value == "":
            return pd.NA

        dtype = self.data[column_name].dtype

        if pd.api.types.is_integer_dtype(dtype):
            return int(value)
        if pd.api.types.is_float_dtype(dtype):
            return float(value)
        return value

    def _on_sheet_edit(self, event_data):
        try:
            row = event_data["row"]
            column = event_data["column"]
            value = event_data["value"]
        except Exception:
            return

        if self.data is None or self.data.empty:
            return

        if row < 0 or column < 0 or row >= len(self.data.index) or column >= len(self.data.columns):
            return

        column_name = self.data.columns[column]
        original_value = self.data.iat[row, column]

        try:
            self.data.iat[row, column] = self._coerce_sheet_value(column_name, value)
        except (ValueError, TypeError):
            CTkMessagebox(title="Error", message=f"Invalid Value Type. Expected {self.data[column_name].dtype}.", icon="cancel", option_1="OK")
            self.records_sheet.set_cell_data(row, column, "" if pd.isna(original_value) else original_value, redraw=False)
            self.records_sheet.refresh()
            return

    def update_record_table(self):
            for widget in self.records_frame.winfo_children():
                widget.destroy()

            if self.data is None or self.data.empty:
                self.records_sheet = None
                empty_label = ctt.CTkLabel(master=self.records_frame, text="No records loaded")
                empty_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
                self.records_frame.grid_columnconfigure(0, weight=1)
                self.records_frame.grid_rowconfigure(0, weight=1)
                return

            self.records_frame.grid_columnconfigure(0, weight=1)
            self.records_frame.grid_rowconfigure(0, weight=1)

            sheet_data = self.data.fillna("").astype(str).values.tolist()
            headers = [str(marker) for marker in self.data.columns]

            self.records_sheet = Sheet(
                self.records_frame,
                data=sheet_data,
                headers=headers,
                show_row_index=False,
                show_header=True,
                show_x_scrollbar=True,
                show_y_scrollbar=True,
                **self._sheet_theme_kwargs(),
            )
            self.records_sheet.grid(row=0, column=0, sticky="nsew")
            self.records_sheet.basic_bindings(True)
            self.records_sheet.extra_bindings("end_edit_cell", self._on_sheet_edit)
            self.records_sheet.enable_bindings()
            self.records_sheet.refresh()


    def select_template(self):
        file = filedialog.askopenfilename(title=self.lang.get("select_template"), filetypes=[("Word Documents", "*.docx")])
        if file:
            self.doc_path = file
            template_name_entry = ctt.CTkEntry(master=self.template_section_frame)
            template_name_entry.insert(0, f"{path.basename(file)}")
            #filename readonly
            template_name_entry.configure(state="readonly")
            template_name_entry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
            print(f"Selected template: {self.doc_path}")
    def select_output(self):
        folder = filedialog.askdirectory(title=self.lang.get("select_output_folder"))
        if folder:
            self.output_folder = folder
            output_folder_entry = ctt.CTkEntry(master=self.template_section_frame)
            output_folder_entry.insert(0, f"{path.basename(folder)}")
            output_folder_entry.configure(state="readonly")
            output_folder_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
            print(f"Selected output folder: {self.output_folder}")
    def import_data(self):
        if self.extract_checkbox_changed() and not self.markers:
            CTkMessagebox(title="Error", message=self.lang.get("no_markers_available"), icon="cancel", option_1="OK")
            return
        data_file = list(filedialog.askopenfilenames(title="Select Data File", filetypes=[("Data Files", ("*.csv", "*.xlsx", "*.docx")), ("All Files", "*.*")]))

        if not data_file:
            return


        for item in data_file:
            ext = item.split(".")[-1].lower()
            imported_data = None

            if ext == "xlsx":
                filename = path.basename(item)
                input_dialog = customtkinter.CTkInputDialog(title=self.lang.get("excel_detected"), text=f"Name: {filename}\n {self.lang.get('excel_file_row_input')}:")
                row_input = input_dialog.get_input()
                if row_input is None:
                    return

                try:
                    table_number = int(row_input)
                    imported_data = DataProcess.get_data(item, skiprows=table_number - 1)
                except ValueError:
                    CTkMessagebox(title="Error", message=self.lang.get("invalid_number"), icon="cancel", option_1="OK")
                    return
            # If the file is a DOCX, let the user choose the table to import.
            elif ext == "docx":
                if self.extract_checkbox_changed():
                    raw_data = DataProcess.get_data(item, from_markers=self.markers)
                    
                    if raw_data and len(raw_data) > 0:
                        imported_data = raw_data[0]
                    else:
                        imported_data = pd.DataFrame()
                        
                else:
                    raw_data = DataProcess.get_data(item)

                    if len(raw_data) > 1:
                        selector = TableSelector(self.root, raw_data)
                        self.root.wait_window(selector)
                        target_index = selector.selected_index

                        if target_index is None:
                            return
                        imported_data = raw_data[target_index]
                    # If there is only one table, use it without asking.
                    elif len(raw_data) == 1:
                        imported_data = raw_data[0]
                    # If no tables were found, skip this file.
                    else:
                        imported_data = pd.DataFrame()
            else:
                imported_data = DataProcess.get_data(item)

            if imported_data is None or imported_data.empty:
                continue
            if self.data is not None and not self.data.empty:
                current_columns = [str(col).strip().replace(" ", "_") for col in self.data.columns]
                
                if current_columns != list(imported_data.columns):
                    CTkMessagebox(
                        title="Warning",
                        message=f"The file {path.basename(item)} was skipped because its columns do not match the current markers.",
                        icon="warning",
                        option_1="OK",
                    )
                    continue

                # Matching markers mean the new rows can be safely concatenated.
                self.data = pd.concat([self.data, imported_data], ignore_index=True)
            else:
                # No data is loaded yet, so use this file as the starting dataset.
                self.data = imported_data

            remove_empty_columns_button = ctt.CTkButton(master=self.data_frame, text=self.lang.get("remove_empty_columns"), command=self.remove_empty_columns)
            remove_empty_columns_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")
            # Show the imported file name in the UI.
            data_name_entry = ctt.CTkEntry(master=self.data_frame)
            data_name_entry.insert(0, f"{path.basename(item)}")
            data_name_entry.configure(state="readonly")
            data_name_entry.grid(row=1, column=1, sticky="ew")
        clean_columns = []
        for col in self.data.columns:
            name = str(col).strip().replace(" ", "_")
            name = name.replace(":", "")
            clean_columns.append(name)
        self.data.columns = clean_columns
        self.markers = list(self.data.columns)
        self.update_markers_grid()
        self.update_record_table()

    def remove_empty_columns(self):
        if self.data is not None and not self.data.empty:
            #replace the empty values with nan
            self.data.replace("", pd.NA, inplace=True)
            self.data.dropna( how='all', inplace=True)    
            self.data.dropna(axis=1, how='all', inplace=True)
            self.markers = list(self.data.columns)
            self.update_markers_grid()
            self.update_record_table()
    def remove_empty_rows(self):
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
        self.remove_all_markers()
        self.update_markers_grid()
    
    def add_record_manually(self):
        if(self.markers is None or len(self.markers) == 0):
            CTkMessagebox(title="Error", message=self.lang.get("no_markers_available"), icon="cancel", option_1="OK")
            return
        #open a new window with a table to add the data manually, the table will have two columns: "Marker" and "Value", and a button to save the data, when you click the button, it will save the data in a dictionary, the key of the dictionary will be the marker and the value of the dictionary will be the value you provided
        manual_data_window = ctt.CTkToplevel(self.root)
        manual_data_window.title("Add Data Manually")
        manual_data_window.geometry("400x400")
        manual_data_window.grid_columnconfigure(0, weight=1)
        manual_data_window.grid_rowconfigure(0, weight=1)
        table_frame = ctt.CTkScrollableFrame(manual_data_window)
        table_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_columnconfigure(1, weight=1)
        table_frame.grid_rowconfigure(0, weight=0)
        marker_label = ctt.CTkLabel(table_frame, text=self.lang.get("marker"), font=ctt.CTkFont(weight="bold"))
        value_label = ctt.CTkLabel(table_frame, text=self.lang.get("value"), font=ctt.CTkFont(weight="bold"))
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
            if(self.data is None) or self.markers is None or len(self.markers) == 0:
                CTkMessagebox(title="Error", message=self.lang.get("no_markers_available"), icon="cancel", option_1="OK")
                return
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
        if self.records_sheet is None or self.data is None or self.data.empty:
            CTkMessagebox(title="Error", message=self.lang.get("no_records_loaded"), icon="cancel", option_1="OK")
            return

        selected_rows = sorted(self.records_sheet.get_selected_rows())
        if not selected_rows:
            CTkMessagebox(title="Error", message=self.lang.get("no_records_selected"), icon="cancel", option_1="OK")
            return
        print(f"Selected indices for deletion: {selected_rows}")
        confirm = CTkMessagebox(title=self.lang.get("confirm_deletion"), message=self.lang.get("confirm_deletion_message").format(num_records=len(selected_rows)), icon="warning", option_2=self.lang.get("no"), option_1=self.lang.get("yes"))
        if confirm.get() == self.lang.get("yes"):
            self.data.drop(index=selected_rows, inplace=True)
            self.data.reset_index(drop=True, inplace=True)
            self.update_record_table()

    def generate_documents(self):
        if self.doc_path is None:
            CTkMessagebox(title="Error", message=self.lang.get("no_template_selected"), icon="cancel", option_1="OK")
            return
        if self.data is None or self.data.empty:
            CTkMessagebox(title="Error", message=self.lang.get("no_data_loaded"), icon="cancel", option_1="OK")
            return
        if not getattr(self, "output_folder", None):
            CTkMessagebox(title="Error", message="Select an output folder first.", icon="cancel", option_1="OK")
            return
        #generate the documents using the template and the data, and save them in the output folder
        file_manager = FileManager(template=self.doc_path, output_folder=self.output_folder, markers=self.markers)
        generated_files = file_manager.generate_documents(self.data)
        CTkMessagebox(title="Success", message=f"Generated {len(generated_files)} document(s).", icon="check", option_1="OK")