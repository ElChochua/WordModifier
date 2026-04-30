import tkinter as tk
from tkinter import messagebox
root = tk.Tk()

def solve():
    messagebox.showinfo('Pisos Picados', 'Mi casa')

def main():
    print("donde caemos gente")
    tk.Button(root, text="Picale pa decidir padrino", command=solve).pack()
    root.mainloop()


if __name__ == "__main__":
    main()

