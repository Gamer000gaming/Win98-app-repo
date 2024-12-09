import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageDraw, ImageTk


def open(window):
    PaintApp(window)


class PaintApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Paint")

        # Configuration initiale de la taille de la fenêtre
        self.master.config(width=400, height=300)
        self.master.bind("<Configure>", self.resize_canvas)

        # Variables
        self.active_tool = "brush"  # Outils disponibles : brush, eraser
        self.brush_color = "black"
        self.brush_size = 5
        self.image = Image.new("RGB", (400, 300), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Interface utilisateur
        self.setup_ui()

    def setup_ui(self):
        """Configuration des éléments de l'interface utilisateur."""
        # Cadre supérieur pour les boutons
        self.tool_frame = tk.Frame(self.master, bg="white")
        self.tool_frame.pack(side=tk.TOP, fill=tk.X)

        # Boutons
        tk.Button(self.tool_frame, text="Pinceau", command=lambda: self.set_tool("brush")).pack(side=tk.LEFT, padx=2)
        tk.Button(self.tool_frame, text="Gomme", command=lambda: self.set_tool("eraser")).pack(side=tk.LEFT, padx=2)
        tk.Button(self.tool_frame, text="Couleur", command=self.choose_color).pack(side=tk.LEFT, padx=2)
        tk.Button(self.tool_frame, text="Vider", command=self.clear_canvas).pack(side=tk.LEFT, padx=2)
        tk.Button(self.tool_frame, text="Ouvrir", command=self.open_image).pack(side=tk.LEFT, padx=2)
        tk.Button(self.tool_frame, text="Enregistrer", command=self.save_image).pack(side=tk.LEFT, padx=2)

        # Zone de dessin
        self.canvas = tk.Canvas(self.master, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Événements
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.start_paint)

        # Coordonnées initiales
        self.last_x = None
        self.last_y = None

    def set_tool(self, tool):
        """Définit l'outil actif."""
        self.active_tool = tool

    def choose_color(self):
        """Ouvre un sélecteur de couleurs pour le pinceau."""
        color = colorchooser.askcolor(color=self.brush_color)[1]
        if color:
            self.brush_color = color

    def clear_canvas(self):
        """Réinitialise le canevas et l'image associée."""
        self.canvas.delete("all")
        self.image = Image.new("RGB", self.image.size, "white")
        self.draw = ImageDraw.Draw(self.image)

    def start_paint(self, event):
        """Enregistre les coordonnées initiales pour le dessin."""
        self.last_x = event.x
        self.last_y = event.y

    def paint(self, event):
        """Dessine sur le canevas et met à jour l'image."""
        if self.last_x and self.last_y:
            color = self.brush_color if self.active_tool == "brush" else "white"
            width = self.brush_size if self.active_tool == "brush" else self.brush_size * 2
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=color, width=width, capstyle=tk.ROUND)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=color, width=width)

        self.last_x = event.x
        self.last_y = event.y

    def resize_canvas(self, event):
        """Adapte la taille de l'image et du canevas à la fenêtre."""
        new_width = event.width
        new_height = event.height

        # Redimensionner l'image PIL
        old_image = self.image
        self.image = Image.new("RGB", (new_width, new_height), "white")
        self.image.paste(old_image, (0, 0))

        self.draw = ImageDraw.Draw(self.image)

        # Redimensionner le canevas
        self.canvas.config(width=new_width, height=new_height)

    def open_image(self):
        """Charge une image depuis un fichier."""
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            loaded_image = Image.open(file_path)
            loaded_image = loaded_image.resize(self.image.size, Image.Resampling.LANCZOS)
            self.image.paste(loaded_image, (0, 0))
            self.refresh_canvas()

    def save_image(self):
        """Enregistre l'image actuelle dans un fichier PNG."""
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image.save(file_path)

    def refresh_canvas(self):
        """Met à jour le contenu du canevas en fonction de l'image actuelle."""
        self.canvas.delete("all")
        tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=tk_image)
        self.canvas.image = tk_image  # Évite la suppression de l'image par le garbage collector


if __name__ == "__main__":
    root = tk.Tk()
    PaintApp(root)
    root.mainloop()
