import customtkinter
from Util.MyApp import MyApp
from CTkMessagebox import CTkMessagebox
import customtkinter
root = customtkinter.CTk()

def solve():
    CTkMessagebox(title="Error", message="No se ha seleccionado un archivo de plantilla.", icon="cancel", option_1="OK")
#Spinbox = valores numericos, Entry = Texto al parecer #listbox eso, listas. Frame = contenedor tk.Text = text area
def main():
    app = MyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

