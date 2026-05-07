import customtkinter as ctt

class TableSelector(ctt.CTkToplevel):
    def __init__(self, parent, tables_data):
        super().__init__(parent)
        self.title("Select Table")
        self.geometry("500x400")
        
        self.selected_index = None
        self.grab_set()

        
        label = ctt.CTkLabel(self, text="Several tables were found.\nSelect the one containing the data:", font=("Arial", 14, "bold"))
        label.pack(pady=20)

        scroll_frame = ctt.CTkScrollableFrame(self, width=450, height=250)
        scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)

        for i, table in enumerate(tables_data):

            if hasattr(table, "columns"):
                headers = [str(column) for column in table.columns[:3]]
            else:
                first_row = table[0] if len(table) > 0 else []
                headers = [str(column) for column in first_row[:3]]

            preview_text = f"Table {i+1}: " + " | ".join(headers)
            if len(headers) == 3:
                preview_text += "..." 
            
            btn = ctt.CTkButton(
                master=scroll_frame,
                text=preview_text,
                anchor="w",
                command=lambda idx=i: self.select_table(idx)
            )
            btn.pack(fill="x", pady=5)

    def select_table(self, index):
        self.selected_index = index
        self.destroy() 