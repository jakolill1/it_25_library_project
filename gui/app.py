import tkinter as tk
from tkinter import messagebox, ttk

from gui.form_panel import BookFormPanel
from gui.list_panel import BookListPanel
from gui.stats_panel import StatsPanel  # Importige StatsPanel
from services.library_service import LibraryService


class LibraryApp:
    """Seob kasutajaliidese komponendid ja rakenduse tegevused."""

    def __init__(self, service: LibraryService) -> None:
        """Valmistab peaakna ja kõik alamkomponendid ette."""
        self.service = service
        self.root = tk.Tk()
        self.root.title("Raamatukogu haldur")
        self.root.geometry("1100x620")
        self.root.minsize(980, 560)

        # Formi paneel ja raamatute nimekiri
        self.form_panel = BookFormPanel(self.root)
        self.list_panel = BookListPanel(self.root)

        # Statistika paneel
        self.stats_panel = StatsPanel(self.root, self.service)  # Lisatud stats_panel
        self.stats_panel.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=12)  # Statistika paigutus
        self.stats_panel.update_stats()  # Statistika värskendamine

        self._build_layout()
        self._build_button_row()
        self.refresh_list()

    def run(self) -> None:
        """Käivitab Tkinteri põhisilmuse."""
        self.root.mainloop()

    def add_book(self) -> None:
        """Lisab vormilt saadud andmete põhjal uue raamatu."""
        title, author, year_text, genre = self.form_panel.get_book_form_data()
        success, message = self.service.add_book(title, author, year_text, genre)

        if success:
            self.form_panel.clear_form()
            self.refresh_list()
            self.stats_panel.update_stats()  # Värskenda statistikat raamatu lisamisel
            messagebox.showinfo("Info", message)
            return

        messagebox.showerror("Viga", message)

    def delete_selected_book(self) -> None:
        """Kustutab parajasti valitud raamatu."""
        book_id = self.list_panel.get_selected_book_id()
        if book_id is None:
            messagebox.showwarning("Hoiatus", "Palun vali tabelist raamat.")
            return

        success, message = self.service.delete_book(book_id)
        if success:
            self.refresh_list()
            self.stats_panel.update_stats()  # Värskenda statistikat raamatu kustutamisel
            messagebox.showinfo("Info", message)
            return

        messagebox.showerror("Viga", message)

    def toggle_selected_status(self) -> None:
        """Muudab valitud raamatu staatust."""
        book_id = self.list_panel.get_selected_book_id()
        if book_id is None:
            messagebox.showwarning("Hoiatus", "Palun vali tabelist raamat.")
            return

        success, message = self.service.toggle_book_status(book_id)
        if success:
            self.refresh_list()
            self.stats_panel.update_stats()  # Värskenda statistikat staatuse muutmisel
            messagebox.showinfo("Info", message)
            return

        messagebox.showerror("Viga", message)

    def refresh_list(self) -> None:
        """Värskendab tabeli sisu otsingu ja filtri järgi."""
        query = self.form_panel.get_search_query()
        status_filter = self.form_panel.get_status_filter()
        books = self.service.search_books(query, status_filter)
        self.list_panel.populate(books)

    def _build_layout(self) -> None:
        """Paigutab peamised paneelid aknasse."""
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.form_panel.grid(row=0, column=0, sticky="ns", padx=12, pady=12)
        self.list_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 12), pady=12)

    def _build_button_row(self) -> None:
        """Loob tegevusnupud ja seob need käskudega."""
        button_frame = ttk.Frame(self.form_panel)
        button_frame.grid(row=7, column=0, columnspan=2, sticky="ew", padx=8, pady=(10, 8))
        button_frame.columnconfigure((0, 1), weight=1)

        ttk.Button(button_frame, text="Lisa raamat", command=self.add_book).grid(
            row=0, column=0, sticky="ew", padx=(0, 4), pady=4
        )
        ttk.Button(button_frame, text="Värskenda vaadet", command=self.refresh_list).grid(
            row=0, column=1, sticky="ew", padx=(4, 0), pady=4
        )
        ttk.Button(button_frame, text="Muuda staatust", command=self.toggle_selected_status).grid(
            row=1, column=0, sticky="ew", padx=(0, 4), pady=4
        )
        ttk.Button(button_frame, text="Kustuta valitud", command=self.delete_selected_book).grid(
            row=1, column=1, sticky="ew", padx=(4, 0), pady=4
        )

        # ✅ Uus nupp valitud raamatu andmete uuendamiseks
        ttk.Button(button_frame, text="Uuenda valitud", command=self.update_selected_book).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=4
        )

        self.form_panel.search_entry.bind("<KeyRelease>", lambda _event: self.refresh_list())
        self.form_panel.status_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh_list())

    def update_selected_book(self) -> None:
        """Muudab valitud raamatu andmeid."""
        book_id = self.list_panel.get_selected_book_id()
        if book_id is None:
            messagebox.showwarning("Hoiatus", "Palun vali tabelist raamat.")
            return

        title, author, year_text, genre = self.form_panel.get_book_form_data()
        success, message = self.service.update_book(book_id, title, author, year_text, genre)

        if success:
            self.form_panel.clear_form()
            self.refresh_list()
            self.stats_panel.update_stats()  # Värskenda statistikat raamatu muutmisel
            messagebox.showinfo("Info", message)
            return

        messagebox.showerror("Viga", message)

    def fill_form_from_selection(self, _event=None) -> None:
        """Täidab vormi valitud raamatu andmetega."""
        book_id = self.list_panel.get_selected_book_id()
        if book_id is None:
            return

        book = self.service.find_by_id(book_id)
        if book is None:
            return

        self.form_panel.title_var.set(book.title)
        self.form_panel.author_var.set(book.author)
        self.form_panel.year_var.set(str(book.year))
        self.form_panel.genre_var.set(book.genre)