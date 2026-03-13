import tkinter as tk
from tkinter import ttk

class StatsPanel(ttk.LabelFrame):
    """Kuvab raamatukogu statistikat."""

    def __init__(self, master: tk.Misc, service) -> None:
        super().__init__(master, text="Statistika")
        self.service = service
        self.total_label = ttk.Label(self, text="Raamatute koguarv: 0")
        self.total_label.grid(row=0, column=0, sticky="w", padx=8, pady=6)
        self.columnconfigure(0, weight=1)

    def update_stats(self) -> None:
        total = self.service.get_total_books()
        self.total_label.config(text=f"Raamatute koguarv: {total}")