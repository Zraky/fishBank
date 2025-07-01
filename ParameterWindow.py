import tkinter as tk
from tkinter import ttk, simpledialog
import json
import Setting
import os

CONFIG_FILE = "settings.json"

class ParameterWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Réglages Poissons")
        self.geometry("350x600")
        self.configure(padx=10, pady=10)

        self.vars = {
            "ALIGNMENT_STRENGTH": tk.DoubleVar(),
            "nb_closer_fish": tk.IntVar(),
            "spacing": tk.DoubleVar(),
            "optimal_dist": tk.DoubleVar(),
            "max_dist": tk.DoubleVar(),
            "COHESION_WEIGHT": tk.DoubleVar(),
            "ALIGNMENT_WEIGHT": tk.DoubleVar(),
            "view_fish": tk.IntVar(),
            "refresh": tk.IntVar(),
            "display_shark": tk.BooleanVar(),
        }

        self.build_widgets()
        self.load_settings()
        self.update_values()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_widgets(self):
        row = 0
        for key, var in self.vars.items():
            ttk.Label(self, text=key).grid(row=row, column=0, sticky="w")
            if isinstance(var, (tk.IntVar, tk.DoubleVar)):
                ttk.Scale(self, from_=0, to=500, variable=var,
                          command=lambda e=None: self.update_values(),
                          orient=tk.HORIZONTAL, length=200).grid(row=row, column=1)
            elif isinstance(var, tk.BooleanVar):
                ttk.Checkbutton(self, variable=var, command=self.update_values).grid(row=row, column=1)
            row += 1

        ttk.Label(self, text="display_fish_link (IDs)").grid(row=row, column=0, sticky="w")
        ttk.Button(self, text="Modifier", command=self.edit_fish_link).grid(row=row, column=1)
        row += 1

        ttk.Label(self, text="display_shark_link (IDs)").grid(row=row, column=0, sticky="w")
        ttk.Button(self, text="Modifier", command=self.edit_shark_link).grid(row=row, column=1)

    def update_values(self, _=None):
        Setting.ALIGNMENT_STRENGTH = self.vars["ALIGNMENT_STRENGTH"].get()
        Setting.nb_closer_fish = self.vars["nb_closer_fish"].get()
        Setting.spacing = self.vars["spacing"].get()
        Setting.optimal_dist = self.vars["optimal_dist"].get()
        Setting.max_dist = self.vars["max_dist"].get()
        Setting.COHESION_WEIGHT = self.vars["COHESION_WEIGHT"].get()
        Setting.ALIGNMENT_WEIGHT = self.vars["ALIGNMENT_WEIGHT"].get()
        Setting.view_fish = self.vars["view_fish"].get()
        Setting.refresh = self.vars["refresh"].get()
        Setting.display_shark = self.vars["display_shark"].get()

    def edit_fish_link(self):
        ids_str = simpledialog.askstring("Modifier display_fish_link", "Entrez les IDs séparés par des virgules :",
                                         initialvalue=",".join(map(str, Setting.display_fish_link)))
        if ids_str:
            Setting.display_fish_link = [int(i) for i in ids_str.split(",") if i.strip().isdigit()]

    def edit_shark_link(self):
        ids_str = simpledialog.askstring("Modifier display_shark_link", "Entrez les IDs séparés par des virgules :",
                                         initialvalue=",".join(map(str, Setting.display_shark_link)))
        if ids_str:
            Setting.display_shark_link = [int(i) for i in ids_str.split(",") if i.strip().isdigit()]

    def load_settings(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                for key in self.vars:
                    if key in data:
                        self.vars[key].set(data[key])
                Setting.display_fish_link = data.get("display_fish_link", [])
                Setting.display_shark_link = data.get("display_shark_link", [])

    def save_settings(self):
        data = {key: var.get() for key, var in self.vars.items()}
        data["display_fish_link"] = Setting.display_fish_link
        data["display_shark_link"] = Setting.display_shark_link
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def on_close(self):
        self.save_settings()
        self.destroy()
