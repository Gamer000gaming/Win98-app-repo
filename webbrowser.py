import tkinter as tk
from tkinterweb import HtmlFrame

def open(window):
    BrowserApp(window)

class BrowserApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Navigateur Web")
        self.master.config(width=400, height=300)

        # Cadre principal
        self.container = tk.Frame(master)
        self.container.pack(fill="both", expand=True)

        # Barre d'adresse
        self.address_bar = tk.Entry(self.container)
        self.address_bar.pack(side="top", fill="x")
        self.address_bar.bind("<Return>", self.load_url)  # Appuyer sur "Entrée" charge l'URL

        # Canvas pour défilement
        self.canvas = tk.Canvas(self.container)
        self.canvas.pack(fill="both", expand=True, side="top")

        # Sliders de défilement
        self.h_scroll = tk.Scrollbar(self.container, orient="horizontal", command=self.canvas.xview)
        self.h_scroll.pack(side="bottom", fill="x")
        self.v_scroll = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.v_scroll.pack(side="right", fill="y")
        self.canvas.configure(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)

        # HtmlFrame placé dans le Canvas
        self.html_frame = HtmlFrame(self.canvas, messages_enabled=False)
        self.html_window = self.canvas.create_window(0, 0, anchor="nw", window=self.html_frame)

        # Charger un site web par défaut
        self.html_frame.load_website("https://www.google.com")
        self.update_scroll_region()  # Mettre à jour la région de défilement initiale

        # Redimensionnement et mise à jour du Canvas
        self.master.bind("<Configure>", self.resize_frame)
        self.html_frame.bind("<<DocumentLoaded>>", lambda e: self.update_scroll_region())

    def resize_frame(self, event):
        # Ajuste la taille du Canvas et du HtmlFrame
        new_width = event.width - self.v_scroll.winfo_width()
        new_height = event.height - self.h_scroll.winfo_height() - self.address_bar.winfo_height()
        self.canvas.config(width=new_width, height=new_height)
        self.canvas.itemconfig(self.html_window, width=new_width, height=new_height)

    def update_scroll_region(self):
        # Met à jour la région de défilement du Canvas
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def load_url(self, event):
        # Charge l'URL entrée dans la barre d'adresse
        url = self.address_bar.get()
        if not url.startswith("http"):
            url = "http://" + url  # Ajoute "http://" si nécessaire
        self.html_frame.load_website(url)

if __name__ == "__main__":
    root = tk.Tk()
    BrowserApp(root)
    root.mainloop()
