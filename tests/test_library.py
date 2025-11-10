from datetime import datetime
import pytest
from src.models import Book, Patron, Loan
from src.library import LibrarySystem

def test_add_book():
    library = LibrarySystem()
    book = library.add_book("Test Book", "Test Author", "123-456-789")
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "123-456-789"
    assert book.available == True

def test_add_patron():
    library = LibrarySystem()
    patron = library.add_patron("John Doe", "john@example.com", "123-456-7890")
    assert patron.name == "John Doe"
    assert patron.email == "john@example.com"
    assert patron.phone == "123-456-7890"

def test_borrow_book():
    library = LibrarySystem()
    book = library.add_book("Test Book", "Test Author", "123-456-789")
    patron = library.add_patron("John Doe", "john@example.com", "123-456-7890")
    
    loan = library.borrow_book(book.id, patron.id)
    assert loan is not None
    assert loan.book_id == book.id
    assert loan.patron_id == patron.id
    assert loan.return_date is None

def test_return_book():
    library = LibrarySystem()
    book = library.add_book("Test Book", "Test Author", "123-456-789")
    patron = library.add_patron("John Doe", "john@example.com", "123-456-7890")
    
    loan = library.borrow_book(book.id, patron.id)
    assert library.return_book(book.id) == True
    assert book.available == True
    assert book.borrowed_by is None