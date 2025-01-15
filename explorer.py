import os
import tkinter as tk
from tkinter import simpledialog, messagebox

open_file = open #pour pouvoir ouvrir des fichiers

class FileExplorer(tk.Frame):
    def __init__(self, parent, initial_dir=None):
        super().__init__(parent)
        self.current_dir = initial_dir or os.getcwd()

        self.file_list = tk.Listbox(self, selectmode=tk.SINGLE)
        self.file_list.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.file_list.bind("<Double-1>", self.open_selection)

        scrollbar = tk.Scrollbar(self, command=self.file_list.yview)
        self.file_list.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

        control_frame = tk.Frame(self)
        control_frame.pack(fill=tk.Y, side=tk.RIGHT)

        create_file_btn = tk.Button(control_frame, text="Créer Fichier", command=self.create_file)
        create_file_btn.pack(fill=tk.X, padx=5, pady=5)

        create_folder_btn = tk.Button(control_frame, text="Créer Dossier", command=self.create_folder)
        create_folder_btn.pack(fill=tk.X, padx=5, pady=5)

        go_up_btn = tk.Button(control_frame, text="Remonter", command=self.go_up)
        go_up_btn.pack(fill=tk.X, padx=5, pady=5)

        delete_btn = tk.Button(control_frame, text="Supprimer", command=self.delete_item)
        delete_btn.pack(fill=tk.X, padx=5, pady=5)

        self.populate()

    def populate(self):
        self.file_list.delete(0, tk.END)
        try:
            entries = sorted(os.listdir(self.current_dir), key=str.lower)
            for entry in entries:
                self.file_list.insert(tk.END, entry)
        except PermissionError:
            messagebox.showerror("Erreur", "Impossible d'accéder au dossier.")

    def open_selection(self, event):
        selection = self.file_list.curselection()
        if not selection:
            return
        selected = self.file_list.get(selection[0])
        path = os.path.join(self.current_dir, selected)
        if os.path.isdir(path):
            self.current_dir = path
            self.populate()
        else:
            messagebox.showinfo("Fichier", f"Vous avez sélectionné : {selected}")

    def create_file(self):
        filename = simpledialog.askstring("Créer Fichier", "Nom du fichier :")
        if filename:
            filepath = os.path.join(self.current_dir, filename)
            try:
                open_file(filepath, 'w').close()
                self.populate()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def create_folder(self):
        foldername = simpledialog.askstring("Créer Dossier", "Nom du dossier :")
        if foldername:
            folderpath = os.path.join(self.current_dir, foldername)
            try:
                os.makedirs(folderpath)
                self.populate()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))

    def go_up(self):
        parent_dir = os.path.dirname(self.current_dir)
        if parent_dir and os.path.isdir(parent_dir):
            self.current_dir = parent_dir
            self.populate()

    def delete_item(self):
        selection = self.file_list.curselection()
        if not selection:
            return
        selected = self.file_list.get(selection[0])
        path = os.path.join(self.current_dir, selected)
        if messagebox.askyesno("Confirmer", f"Êtes-vous sûr de vouloir supprimer '{selected}' ?"):
            try:
                if os.path.isdir(path):
                    os.rmdir(path)
                else:
                    os.remove(path)
                self.populate()
            except Exception as e:
                messagebox.showerror("Erreur", str(e))            
def open(root):
    explorer = FileExplorer(root)
    explorer.pack(fill=tk.BOTH, expand=True)
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Explorateur de Fichiers")
    explorer = FileExplorer(root)
    explorer.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

