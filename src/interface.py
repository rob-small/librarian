
"""
interface.py
-------------
This module defines the Gradio-based user interface for the Library Management System.
It provides interactive tabs for adding books and patrons, borrowing and returning books,
and viewing the library status, all backed by the LibrarySystem class.
"""

import gradio as gr
from datetime import datetime
from typing import Tuple
from .library import LibrarySystem


class LibraryInterface:
    """
    Provides high-level methods for interacting with the LibrarySystem.
    Used by the Gradio interface to manage books, patrons, loans, and status queries.
    """
    def __init__(self):
        """
        Initialize the LibraryInterface and add sample data for demonstration.
        """
        self.library = LibrarySystem()
        self._add_sample_data()


    def _add_sample_data(self):
        """
        Add sample books and patrons to the library for demonstration purposes.
        """
        self.library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565")
        self.library.add_book("To Kill a Mockingbird", "Harper Lee", "978-0446310789")
        self.library.add_book("1984", "George Orwell", "978-0451524935")
        self.library.add_patron("John Doe", "john@example.com", "123-456-7890")
        self.library.add_patron("Jane Smith", "jane@example.com", "098-765-4321")


    def add_book(self, title: str, author: str, isbn: str) -> str:
        """
        Add a new book to the library.
        Returns a success message or prompts for missing fields.
        """
        if not all([title, author, isbn]):
            return "Please fill in all fields"
        book = self.library.add_book(title, author, isbn)
        return f"Book added successfully! Book ID: {book.id}"


    def add_patron(self, name: str, email: str, phone: str) -> str:
        """
        Add a new patron to the library.
        Returns a success message or prompts for missing fields.
        """
        if not all([name, email, phone]):
            return "Please fill in all fields"
        patron = self.library.add_patron(name, email, phone)
        return f"Patron added successfully! Patron ID: {patron.id}"


    def borrow_book(self, book_id: str, patron_id: str, loan_days: int) -> str:
        """
        Borrow a book for a patron for a specified number of days.
        Returns a success message with due date or an error message.
        """
        try:
            book_id = int(book_id)
            patron_id = int(patron_id)
        except ValueError:
            return "Please enter valid numeric IDs"
        loan = self.library.borrow_book(book_id, patron_id, loan_days)
        if loan:
            return f"Book borrowed successfully! Due date: {loan.due_date.strftime('%Y-%m-%d')}"
        return "Failed to borrow book. Check if book/patron exists and book is available"


    def return_book(self, book_id: str) -> str:
        """
        Return a borrowed book to the library.
        Returns a success message or an error message.
        """
        try:
            book_id = int(book_id)
        except ValueError:
            return "Please enter a valid numeric book ID"
        success = self.library.return_book(book_id)
        if success:
            return "Book returned successfully!"
        return "Failed to return book. Check if book exists and is borrowed"


    def list_books(self) -> str:
        """
        List all books in the library with their status.
        Returns a formatted string of book details.
        """
        if not self.library.books:
            return "No books in the library"
        book_list = []
        for book in self.library.books:
            status = "Available" if book.available else f"Borrowed by Patron #{book.borrowed_by}"
            book_list.append(
                f"ID: {book.id} | {book.title} by {book.author} | ISBN: {book.isbn} | {status}"
            )
        return "\n".join(book_list)


    def list_patrons(self) -> str:
        """
        List all registered patrons in the library.
        Returns a formatted string of patron details.
        """
        if not self.library.patrons:
            return "No patrons registered"
        patron_list = []
        for patron in self.library.patrons:
            patron_list.append(
                f"ID: {patron.id} | {patron.name} | Email: {patron.email} | Phone: {patron.phone}"
            )
        return "\n".join(patron_list)


    def list_overdue(self) -> str:
        """
        List all overdue loans in the library.
        Returns a formatted string of overdue book and patron details.
        """
        overdue = self.library.get_overdue_loans()
        if not overdue:
            return "No overdue books"
        overdue_list = []
        for loan in overdue:
            book = next(b for b in self.library.books if b.id == loan.book_id)
            patron = next(p for p in self.library.patrons if p.id == loan.patron_id)
            overdue_list.append(
                f"Book: {book.title} (ID: {book.id}) | "
                f"Patron: {patron.name} (ID: {patron.id}) | "
                f"Due date: {loan.due_date.strftime('%Y-%m-%d')}"
            )
        return "\n".join(overdue_list)


def create_interface():
    """
    Build and return the Gradio Blocks interface for the Library Management System.
    Provides tabs for all major library operations.
    """
    interface = LibraryInterface()
    with gr.Blocks(title="Library Management System") as demo:
        gr.Markdown("# Library Management System")
        # ...existing code...
        # Tabs for Add Book, Add Patron, Borrow Book, Return Book, and View Library Status
        # ...existing code...
    return demo


if __name__ == "__main__":
    demo = create_interface()
    demo.launch()