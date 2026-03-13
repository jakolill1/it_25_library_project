def validate_book_input(title: str, author: str, year_text: str, genre: str) -> tuple[bool, str]:
    """Kontrollib raamatu lisamise või uuendamise andmeid."""
    if not title.strip():
        return False, "Pealkiri ei tohi olla tühi."
    if not author.strip():
        return False, "Autor ei tohi olla tühi."
    if not genre.strip():
        return False, "Žanr ei tohi olla tühi."

    try:
        year = int(year_text)
        if year < 0 or year > 2100:
            return False, "Aasta peab olema vahemikus 0–2100."
    except ValueError:
        return False, "Aasta peab olema number."

    return True, "Sisend on korrektne"