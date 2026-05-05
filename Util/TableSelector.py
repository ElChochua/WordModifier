import customtkinter as ctt

class TableSelector(ctt.CTkToplevel):
    def __init__(self, parent, tables_data):
        super().__init__(parent)
        self.title("Seleccionar Tabla")
        self.geometry("500x400")
        
        # Atributo para guardar la elección
        self.selected_index = None
        
        # Hacer que la ventana sea modal (bloquea la principal)
        self.grab_set()
        
        label = ctt.CTkLabel(self, text="Se encontraron varias tablas.\nSelecciona la que contiene los datos:", font=("Arial", 14, "bold"))
        label.pack(pady=20)

        # Contenedor con scroll para las opciones
        scroll_frame = ctt.CTkScrollableFrame(self, width=450, height=250)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        for i, table in enumerate(tables_data):
            # Creamos una previsualización (ej: las primeras 2 filas)
            preview_text = f"Tabla {i+1}: " + " | ".join(table[0][:3]) + "..." # Primeros 3 encabezados
            
            btn = ctt.CTkButton(
                master=scroll_frame,
                text=preview_text,
                anchor="w",
                command=lambda idx=i: self.select_table(idx)
            )
            btn.pack(fill="x", pady=5)

    def select_table(self, index):
        self.selected_index = index
        self.destroy() # Cerramos y devolvemos el control