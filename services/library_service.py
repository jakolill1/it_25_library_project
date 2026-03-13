from __future__ import annotations

from models.book import Book
from services.validators import validate_book_input
from storage.json_storage import JsonStorage

type BookList = list[Book]

class LibraryService:
    """Raamatute haldamise teenus."""

    def __init__(self, storage: JsonStorage) -> None:
        self.storage = storage
        self.books: BookList = self.storage.load_books()

    def get_all_books(self) -> BookList:
        return sorted(self.books, key=lambda book: book.id)

    def add_book(self, title: str, author: str, year_text: str, genre: str) -> tuple[bool, str]:
        is_valid, message = validate_book_input(title, author, year_text, genre)
        if not is_valid:
            return False, message

        new_book = Book(
            id=self._generate_id(),
            title=title.strip(),
            author=author.strip(),
            year=int(year_text.strip()),
            genre=genre.strip(),
            is_borrowed=False,
        )
        self.books.append(new_book)
        self.storage.save_books(self.books)
        return True, "Raamat lisati edukalt."

    def update_book(self, book_id: int, title: str, author: str, year_text: str, genre: str) -> tuple[bool, str]:
        is_valid, message = validate_book_input(title, author, year_text, genre)
        if not is_valid:
            return False, message

        book = self.find_by_id(book_id)
        if book is None:
            return False, "Valitud raamatut ei leitud."

        book.title = title.strip()
        book.author = author.strip()
        book.year = int(year_text.strip())
        book.genre = genre.strip()

        self.storage.save_books(self.books)
        return True, "Raamatu andmed uuendati edukalt."

    def delete_book(self, book_id: int) -> tuple[bool, str]:
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.storage.save_books(self.books)
                return True, "Raamat kustutati edukalt."
        return False, "Valitud raamatut ei leitud."

    def toggle_book_status(self, book_id: int) -> tuple[bool, str]:
        book = self.find_by_id(book_id)
        if book is None:
            return False, "Valitud raamatut ei leitud."
        book.is_borrowed = not book.is_borrowed
        self.storage.save_books(self.books)
        return True, f"Raamatu uus staatus: {book.status_label}."

    def find_by_id(self, book_id: int) -> Book | None:
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def search_books(self, query: str, status_filter: str = "Kõik") -> BookList:
        normalized_query = query.strip().casefold()
        filtered_books = self._apply_status_filter(self.books, status_filter)

        if not normalized_query:
            return sorted(filtered_books, key=lambda book: book.id)

        result = [
            book
            for book in filtered_books
            if normalized_query in book.title.casefold() or normalized_query in book.author.casefold()
        ]
        return sorted(result, key=lambda book: book.id)

    def reload(self) -> None:
        self.books = self.storage.load_books()

    def get_total_books(self) -> int:
        """Tagastab raamatute koguarvu."""
        return len(self.books)

    def _generate_id(self) -> int:
        if not self.books:
            return 1
        return max(book.id for book in self.books) + 1

    def _apply_status_filter(self, books: BookList, status_filter: str) -> BookList:
        match status_filter:
            case "Kohal":
                return [book for book in books if not book.is_borrowed]
            case "Väljas":
                return [book for book in books if book.is_borrowed]
            case _:
                return list(books)

    def get_total_books(self) -> int:
        """Tagastab raamatute koguarvu."""
        return len(self.books)

