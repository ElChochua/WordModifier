import tkinter as tk
from tkinter import PhotoImage
from tkinter import Spinbox
from CTkMessagebox import CTkMessagebox
from os import path
import customtkinter as ctt
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

        self.root.grid_columnconfigure(0, weight=0, minsize=290) 
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

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
        select_file_button = ctt.CTkButton(master=self.template_section_frame, text="Select Doc")
        select_file_label = ctt.CTkLabel(master=self.template_section_frame, text="Template")
        template_name_entry = ctt.CTkEntry(master=self.template_section_frame)
        template_name_entry.insert(0, "Template Name")
        #filename readonly
        template_name_entry.configure(state="readonly")

        select_file_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        select_file_button.grid(row=1, column=0, padx=5, pady=5)
        template_name_entry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
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
        data_import_button = ctt.CTkButton(master=self.data_frame, text="Import Data",image=data_icon, compound="left")
        manual_data_button = ctt.CTkButton(master=self.data_frame, text="Add Data Manually", image=no_data_icon, compound="left")
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
        delete_all_records_button = ctt.CTkButton(master=self.records_section_frame, text="Clear All")
        delete_selected_record_button = ctt.CTkButton(master=self.records_section_frame, text="Delete Selected Record")

        delete_all_records_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")
        delete_selected_record_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        records_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.records_section_frame.grid(row=1, column=1, sticky="nsew")
        #records section
        horizontal_scroll = ctt.CTkScrollbar(master=self.records_frame, orientation="horizontal")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")
        self.records_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")


    def add_marker(self, marker):
        if marker in self.markers:
            CTkMessagebox(title="Error", message="Marker already exists", icon="cancel")
            return
        elif marker.strip() == "":
            CTkMessagebox(title="Error", message="Marker cannot be empty", icon="cancel")
            return
        self.markers.append(marker)
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
            print(f"Number of markers remaining: {(self.markers)}")
            #remove button with marker name

            for widget in self.markers_section_frame.grid_slaves():
                if isinstance(widget, ctt.CTkButton) and widget.cget("text") == marker:
                    widget.destroy()
                    break
            self.update_markers_grid()
            #remove data associated with the marker
            if marker in self.data:
                del self.data[marker]

    def remove_all_markers(self):
        for marker in self.markers[:]:
            self.remove_marker(marker)

    def on_marker_entry(self, event):
        marker = event.widget.get()
        self.add_marker(marker)
        print(f"Number of markers: {(self.markers)}")
        event.widget.delete(0, tk.END)
    def add_record(self, record_data):

        pass