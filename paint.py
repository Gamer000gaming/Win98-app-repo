import tkinter as tk
from tkinter import colorchooser

def open(window):
    PaintApp(window)

class PaintApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Paint")
        self.master.config(width=300, height=200)  # Taille de la fenêtre ajustée

        # Cadre pour les boutons
        self.tool_frame = tk.Frame(self.master, bg="white", height=20)
        self.tool_frame.pack(side=tk.TOP, fill=tk.X)

        # Ajout des boutons (seulement les essentiels pour une petite interface)
        self.brush_button = tk.Button(self.tool_frame, text="Pinceau", command=lambda: self.set_tool("brush"))
        self.eraser_button = tk.Button(self.tool_frame, text="Gomme", command=lambda: self.set_tool("eraser"))
        self.clear_button = tk.Button(self.tool_frame, text="Vider", command=self.clear_canvas)
        self.color_button = tk.Button(self.tool_frame, text="Couleur", command=self.choose_color)

        self.brush_button.pack(side=tk.LEFT, padx=1, pady=1)
        self.eraser_button.pack(side=tk.LEFT, padx=1, pady=1)
        self.color_button.pack(side=tk.LEFT, padx=1, pady=1)
        self.clear_button.pack(side=tk.LEFT, padx=1, pady=1)

        # Zone de dessin
        self.canvas = tk.Canvas(self.master, bg="white", width=100, height=80, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Événements pour dessiner
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.start_paint)

        # Coordonnées initiales
        self.last_x = None
        self.last_y = None

        # Outils
        self.brush_color = "black"
        self.brush_size = 3
        self.active_tool = "brush"  # Outils disponibles : brush, eraser

    def set_tool(self, tool):
        """Change l'outil actif."""
        self.active_tool = tool

    def choose_color(self):
        """Ouvre un sélecteur de couleurs."""
        color = colorchooser.askcolor(color=self.brush_color)[1]
        if color:
            self.brush_color = color

    def clear_canvas(self):
        """Efface tout sur le canevas."""
        self.canvas.delete("all")

    def start_paint(self, event):
        """Enregistre les coordonnées initiales."""
        self.last_x = event.x
        self.last_y = event.y

    def paint(self, event):
        """Dessine sur le canevas."""
        if self.last_x and self.last_y:
            if self.active_tool == "brush":
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        fill=self.brush_color, width=self.brush_size, capstyle=tk.ROUND)
            elif self.active_tool == "eraser":
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        fill="white", width=self.brush_size * 2, capstyle=tk.ROUND)

        self.last_x = event.x
        self.last_y = event.y
