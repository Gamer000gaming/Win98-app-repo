import tkinter as tk
from tkinterweb import HtmlFrame

def open(window):
    BrowserApp(window)

class BrowserApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Navigateur Web")

        # Configuration initiale de la fenêtre avec 400x300 par défaut
        self.master.config(width=400, height=300)
        
        # Création de l'objet HtmlFrame
        self.html_frame = HtmlFrame(master)
        self.html_frame.pack(fill="both", expand=True)
        self.html_frame.load_website("https://www.google.com")
        
        # Redimensionnement dynamique
        self.master.bind("<Configure>", self.resize_frame)

    def resize_frame(self, event):
        # Ajuste la taille du HtmlFrame selon la fenêtre
        self.html_frame.config(width=event.width, height=event.height)

if __name__ == "__main__":
    root = tk.Tk()
    BrowserApp(root)
    root.mainloop()
