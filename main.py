import customtkinter
from Util.MyApp import MyApp
from Util import FileManager
from CTkMessagebox import CTkMessagebox
import customtkinter
import pandas as pd
from Util import DataProcess
root = customtkinter.CTk()

def solve():
    CTkMessagebox(title="Error", message="No se ha seleccionado un archivo de plantilla.", icon="cancel", option_1="OK")
#Spinbox = valores numericos, Entry = Texto al parecer #listbox eso, listas. Frame = contenedor tk.Text = text area
def main():
    app = MyApp(root)
    # documento = "C:\\Users\\jossu\\Downloads\\IOS-Android_v0.2.docx"
    #dp = DataProcess(documento)
    #datasets = dp.read_data()
    #print(datasets)
    root.mainloop()


if __name__ == "__main__":
    main()

