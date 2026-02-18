import unittest
from datetime import date, timedelta
from library import Library, Book, Member
from exceptions import CheckoutRuleViolation, BookNotFoundError, MemberNotFoundError

class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        self.library = Library()

        # ---------- Books ----------
        self.book1 = Book("111", "The Great Gatsby", "F. Scott Fitzgerald")
        self.book2 = Book("222", "Harry Potter", "J.K. Rowling")
        self.book3 = Book("333", "The Immortals of Meluha", "Amish Tripathi")
        self.book4 = Book("444", "The Secret of the Nagas", "Amish Tripathi")
        for book in [self.book1, self.book2, self.book3, self.book4]:
            self.library.add_book(book)

        # ---------- Members ----------
        self.member = Member("M1", "Sonu")
        self.library.register_member(self.member)

    # ---------- Checkout Tests ----------
    def test_checkout_book_success(self):
        self.library.checkout_book("M1", "111")
        self.assertFalse(self.book1.is_available)
        self.assertEqual(len(self.member.current_borrowed), 1)

    def test_checkout_more_than_max_books(self):
        for isbn in ["111", "222", "333"]:
            self.library.checkout_book("M1", isbn)
        with self.assertRaises(CheckoutRuleViolation):
            self.library.checkout_book("M1", "444")

    def test_checkout_with_high_fine(self):
        self.member.fine_balance = 15.0
        with self.assertRaises(CheckoutRuleViolation):
            self.library.checkout_book("M1", "111")

    def test_checkout_nonexistent_book(self):
        with self.assertRaises(BookNotFoundError):
            self.library.checkout_book("M1", "999")

    def test_checkout_nonexistent_member(self):
        with self.assertRaises(MemberNotFoundError):
            self.library.checkout_book("M999", "111")

    # ---------- Return Tests ----------
    def test_return_book_success(self):
        self.library.checkout_book("M1", "111")
        self.library.return_book("M1", "111")
        self.assertTrue(self.book1.is_available)
        self.assertEqual(len(self.member.current_borrowed), 0)

    def test_return_book_not_borrowed(self):
        with self.assertRaises(CheckoutRuleViolation):
            self.library.return_book("M1", "111")

    def test_return_nonexistent_book(self):
        with self.assertRaises(BookNotFoundError):
            self.library.return_book("M1", "999")

    def test_return_nonexistent_member(self):
        with self.assertRaises(MemberNotFoundError):
            self.library.return_book("M999", "111")

    def test_return_book_late_fine(self):
        past_date = date.today() - timedelta(days=20)  # 6 days overdue
        self.library.checkout_book("M1", "111", checkout_date=past_date)
        self.library.return_book("M1", "111", return_date=date.today())
        self.assertEqual(self.member.fine_balance, 3.0)

    # ---------- Fine Calculation ----------
    def test_calculate_fine_with_unreturned_books(self):
        past_date = date.today() - timedelta(days=20)
        self.library.checkout_book("M1", "111", checkout_date=past_date)
        total_fine = self.library.calculate_fine("M1")
        self.assertEqual(total_fine, 3.0)

    # ---------- Borrowing History ----------
    def test_borrowing_history(self):
        self.library.checkout_book("M1", "111")
        self.library.checkout_book("M1", "222")
        self.library.return_book("M1", "111")
        history = self.library.get_member_borrowing_history("M1")
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].book.title, "The Great Gatsby")
        self.assertEqual(history[0].return_date, date.today())
        self.assertEqual(history[1].book.title, "Harry Potter")
        self.assertIsNone(history[1].return_date)
    
    # ---------- Return Date Validation ----------
    def test_return_date_before_checkout_date(self):
        checkout_date = date(2026, 1, 10)
        self.library.checkout_book("M1", "111", checkout_date=checkout_date)
        invalid_return_date = date(2026, 1, 5)
        with self.assertRaises(CheckoutRuleViolation) as context:
            self.library.return_book("M1", "111", return_date=invalid_return_date)
        self.assertIn("Return date", str(context.exception))

    # ---------- Edge Cases ----------
    def test_borrowing_history_empty(self):
        history = self.library.get_member_borrowing_history("M1")
        self.assertEqual(len(history), 0)

    def test_available_books_list(self):
        self.library.checkout_book("M1", "111")
        available = self.library.get_available_books()
        self.assertNotIn(self.book1, available)
        self.assertIn(self.book2, available)

    def test_checkout_and_return_same_day(self):
        self.library.checkout_book("M1", "111")
        self.library.return_book("M1", "111", return_date=date.today())
        self.assertEqual(self.member.fine_balance, 0.0)

if __name__ == "__main__":
    unittest.main()