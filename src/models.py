from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Book:
    id: int
    title: str
    author: str
    isbn: str
    available: bool = True
    borrowed_by: Optional[int] = None

@dataclass
class Patron:
    id: int
    name: str
    email: str
    phone: str

@dataclass
class Loan:
    id: int
    book_id: int
    patron_id: int
    loan_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None