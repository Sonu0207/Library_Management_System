from datetime import date, timedelta
from exceptions import BookNotFoundError, MemberNotFoundError, CheckoutRuleViolation

# ---------------- Constants ----------------
MAX_BORROWED_BOOKS = 3
LOAN_PERIOD_DAYS = 14
FINE_PER_DAY = 0.50
MAX_FINE_ALLOWED = 10.0

# ---------------- Book ----------------
class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.is_available = True
        self.borrower_id = None  # ID of member who borrowed the book

    def __repr__(self):
        return f"{self.title} ({self.isbn})"

# ---------------- BorrowedBook ----------------
class BorrowedBook:
    def __init__(self, book, checkout_date):
        self.book = book
        self.checkout_date = checkout_date
        self.due_date = checkout_date + timedelta(days=LOAN_PERIOD_DAYS)
        self.return_date = None

    def overdue_days(self, today=date.today()):
        check_date = self.return_date or today
        overdue = (check_date - self.due_date).days
        return max(0, overdue)

# ---------------- Member ----------------
class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.current_borrowed = []    # Books currently borrowed
        self.borrowing_history = []   # All borrowings
        self.fine_balance = 0.0

    def can_borrow(self):
        if len(self.current_borrowed) >= MAX_BORROWED_BOOKS:
            return False
        if self.fine_balance > MAX_FINE_ALLOWED:
            return False
        return True

    def borrow_book(self, book, checkout_date=None):
        if not self.can_borrow():
            raise CheckoutRuleViolation(f"Member {self.member_id} cannot borrow more books or has unpaid fines")
        if not book.is_available:
            raise CheckoutRuleViolation(f"Book {book.isbn} is not available")

        if checkout_date is None:
            checkout_date = date.today()

        borrowed = BorrowedBook(book, checkout_date)
        self.current_borrowed.append(borrowed)
        self.borrowing_history.append(borrowed)
        book.is_available = False
        book.borrower_id = self.member_id

    def return_book(self, book, return_date=None):
        for borrowed in self.current_borrowed:
            if borrowed.book.isbn == book.isbn:
                if return_date is None:
                    return_date = date.today()
                
                # ---------- Validation ----------
                if return_date < borrowed.checkout_date:
                    raise CheckoutRuleViolation(
                        f"Return date {return_date} cannot be before checkout date {borrowed.checkout_date}"
                    )
                
                borrowed.return_date = return_date
                overdue_fine = borrowed.overdue_days() * FINE_PER_DAY
                self.fine_balance += overdue_fine
                borrowed.book.is_available = True
                borrowed.book.borrower_id = None
                self.current_borrowed.remove(borrowed)
                return

        raise CheckoutRuleViolation(f"Book {book.isbn} was not borrowed by member {self.member_id}")

    def calculate_total_fine(self):
        total = self.fine_balance
        for borrowed in self.current_borrowed:
            total += borrowed.overdue_days() * FINE_PER_DAY
        return round(total, 2)
    
    

# ---------------- Library ----------------
class Library:
    def __init__(self):
        self.books = {}    # isbn -> Book
        self.members = {}  # member_id -> Member

    # ---------- Book & Member Management ----------
    def add_book(self, book):
        self.books[book.isbn] = book

    def register_member(self, member):
        self.members[member.member_id] = member

    def _get_book(self, isbn):
        if isbn not in self.books:
            raise BookNotFoundError(f"Book {isbn} not found")
        return self.books[isbn]

    def _get_member(self, member_id):
        if member_id not in self.members:
            raise MemberNotFoundError(f"Member {member_id} not found")
        return self.members[member_id]

    # ---------- Borrowing Operations ----------
    def checkout_book(self, member_id, isbn, checkout_date=None):
        member = self._get_member(member_id)
        book = self._get_book(isbn)
        member.borrow_book(book, checkout_date)

    def return_book(self, member_id, isbn, return_date=None):
        member = self._get_member(member_id)
        book = self._get_book(isbn)
        member.return_book(book, return_date)

    def calculate_fine(self, member_id):
        member = self._get_member(member_id)
        return member.calculate_total_fine()

    # ---------- Queries ----------
    def get_available_books(self):
        return [b for b in self.books.values() if b.is_available]

    def get_member_borrowing_history(self, member_id):
        return self._get_member(member_id).borrowing_history

# ---------------- Printing Utilities ----------------
def print_books(library):
    print("\nBooks in Library:")
    for book in library.books.values():
        status = "Available" if book.is_available else f"Checked Out by {book.borrower_id}"
        print(f"- {book.isbn} | {book.title} | {book.author} | {status}")

def print_members(library):
    print("\nMembers:")
    for m in library.members.values():
        print(f"- {m.member_id} | {m.name} | Borrowed: {len(m.current_borrowed)} | Fine: ${m.fine_balance:.2f}")