
"""
models.py
---------
Defines the core data models for the Library Management System: Book, Patron, and Loan.
Uses Python dataclasses for simplicity and type safety.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Book:
    """
    Represents a book in the library.
    Attributes:
        id: Unique identifier for the book.
        title: Title of the book.
        author: Author of the book.
        isbn: ISBN number.
        available: Whether the book is available for borrowing.
        borrowed_by: Patron ID who borrowed the book, if any.
    """
    id: int
    title: str
    author: str
    isbn: str
    available: bool = True
    borrowed_by: Optional[int] = None


@dataclass
class Patron:
    """
    Represents a library patron.
    Attributes:
        id: Unique identifier for the patron.
        name: Patron's name.
        email: Patron's email address.
        phone: Patron's phone number.
    """
    id: int
    name: str
    email: str
    phone: str


@dataclass
class Loan:
    """
    Represents a loan of a book to a patron.
    Attributes:
        id: Unique identifier for the loan.
        book_id: ID of the borrowed book.
        patron_id: ID of the patron who borrowed the book.
        loan_date: Date when the book was borrowed.
        due_date: Date when the book is due to be returned.
        return_date: Date when the book was returned (None if not yet returned).
    """
    id: int
    book_id: int
    patron_id: int
    loan_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None