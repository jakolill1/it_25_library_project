from __future__ import annotations
from gui.stats_panel import StatsPanel
import tkinter as tk
from tkinter import ttk


class BookFormPanel(ttk.LabelFrame):
    """Kuvab raamatu lisamise ja otsingu sisestusväljad."""

    def __init__(self, master: tk.Misc) -> None:
        """Loob kõik vormi sisestusväljad ja filtrid."""
        super().__init__(master, text="Raamatud")

        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.genre_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.status_filter_var = tk.StringVar(value="Kõik")

        self.columnconfigure(1, weight=1)
        self._build_widgets()

    def get_book_form_data(self) -> tuple[str, str, str, str]:
        """Tagastab lisamisvormi väljade väärtused."""
        return (
            self.title_var.get(),
            self.author_var.get(),
            self.year_var.get(),
            self.genre_var.get(),
        )

    def get_search_query(self) -> str:
        """Tagastab otsinguvälja teksti."""
        return self.search_var.get()

    def get_status_filter(self) -> str:
        """Tagastab valitud staatusefiltri."""
        return self.status_filter_var.get()

    def clear_form(self) -> None:
        """Tühjendab raamatu lisamise vormi väljad."""
        self.title_var.set("")
        self.author_var.set("")
        self.year_var.set("")
        self.genre_var.set("")

    def _build_widgets(self) -> None:
        """Paigutab vormi nähtavad komponendid aknasse."""
        ttk.Label(self, text="Pealkiri:").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        ttk.Entry(self, textvariable=self.title_var).grid(row=0, column=1, sticky="ew", padx=8, pady=6)

        ttk.Label(self, text="Autor:").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        ttk.Entry(self, textvariable=self.author_var).grid(row=1, column=1, sticky="ew", padx=8, pady=6)

        ttk.Label(self, text="Aasta:").grid(row=2, column=0, sticky="w", padx=8, pady=6)
        ttk.Entry(self, textvariable=self.year_var).grid(row=2, column=1, sticky="ew", padx=8, pady=6)

        ttk.Label(self, text="Žanr:").grid(row=3, column=0, sticky="w", padx=8, pady=6)
        ttk.Entry(self, textvariable=self.genre_var).grid(row=3, column=1, sticky="ew", padx=8, pady=6)

        ttk.Separator(self).grid(row=4, column=0, columnspan=2, sticky="ew", padx=8, pady=8)

        ttk.Label(self, text="Otsing:").grid(row=5, column=0, sticky="w", padx=8, pady=6)
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_entry.grid(row=5, column=1, sticky="ew", padx=8, pady=6)

        ttk.Label(self, text="Staatus:").grid(row=6, column=0, sticky="w", padx=8, pady=6)
        self.status_box = ttk.Combobox(
            self,
            textvariable=self.status_filter_var,
            state="readonly",
            values=("Kõik", "Kohal", "Väljas"),
        )
        self.status_box.grid(row=6, column=1, sticky="ew", padx=8, pady=6)
