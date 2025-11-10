from datetime import datetime, timedelta
from typing import List, Optional
from .models import Book, Patron, Loan

class LibrarySystem:
    def __init__(self):
        self.books: List[Book] = []
        self.patrons: List[Patron] = []
        self.loans: List[Loan] = []
        self._book_id_counter = 1
        self._patron_id_counter = 1
        self._loan_id_counter = 1

    def add_book(self, title: str, author: str, isbn: str) -> Book:
        book = Book(
            id=self._book_id_counter,
            title=title,
            author=author,
            isbn=isbn
        )
        self.books.append(book)
        self._book_id_counter += 1
        return book

    def add_patron(self, name: str, email: str, phone: str) -> Patron:
        patron = Patron(
            id=self._patron_id_counter,
            name=name,
            email=email,
            phone=phone
        )
        self.patrons.append(patron)
        self._patron_id_counter += 1
        return patron

    def borrow_book(self, book_id: int, patron_id: int, days: int = 14) -> Optional[Loan]:
        book = next((b for b in self.books if b.id == book_id), None)
        patron = next((p for p in self.patrons if p.id == patron_id), None)

        if not book or not patron:
            return None

        if not book.available:
            return None

        loan_date = datetime.now()
        due_date = loan_date + timedelta(days=days)
        
        loan = Loan(
            id=self._loan_id_counter,
            book_id=book_id,
            patron_id=patron_id,
            loan_date=loan_date,
            due_date=due_date
        )

        book.available = False
        book.borrowed_by = patron_id
        
        self.loans.append(loan)
        self._loan_id_counter += 1
        return loan

    def return_book(self, book_id: int) -> bool:
        book = next((b for b in self.books if b.id == book_id), None)
        if not book or book.available:
            return False

        active_loan = next(
            (l for l in self.loans 
             if l.book_id == book_id and l.return_date is None),
            None
        )

        if not active_loan:
            return False

        active_loan.return_date = datetime.now()
        book.available = True
        book.borrowed_by = None
        return True

    def get_patron_loans(self, patron_id: int) -> List[Loan]:
        return [loan for loan in self.loans if loan.patron_id == patron_id]

    def get_overdue_loans(self) -> List[Loan]:
        now = datetime.now()
        return [
            loan for loan in self.loans
            if loan.return_date is None and loan.due_date < now
        ]