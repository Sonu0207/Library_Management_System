from library import Library, Book, Member, print_books, print_members
from datetime import date

# Initialize library
library = Library()

# ---------- Sample Data ----------
books = [
    Book("101", "Book 1", "Author 1"),
    Book("102", "Book 2", "Author 2"),
    Book("103", "Book 3", "Author 3"),
]
for book in books:
    library.add_book(book)

members = [
    Member("M101", "Sonu Tejwani"),
    Member("M102", "Elon Musk"),
]
for member in members:
    library.register_member(member)

# ---------- Menu Loop ----------
while True:
    # Always show books and members
    print("\n===== Library Books =====")
    print_books(library)
    print("\n===== Library Members =====")
    print_members(library)

    # Menu for actions
    print("\n===== Library Menu =====")
    print("1. Add Book")
    print("2. Add Member")
    print("3. Checkout Book")
    print("4. Return Book")
    print("5. Calculate Fine")
    print("6. View Borrowing History")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        isbn = input("Enter ISBN: ")
        title = input("Enter Book Title: ")
        author = input("Enter Author: ")
        library.add_book(Book(isbn, title, author))
        print("Book added successfully!")

    elif choice == "2":
        member_id = input("Enter Member ID: ")
        name = input("Enter Member Name: ")
        library.register_member(Member(member_id, name))
        print("Member added successfully!")

    elif choice == "3":
        member_id = input("Enter Member ID: ")
        isbn = input("Enter Book ISBN: ")
        use_custom_date = input("Use custom checkout date? (y/n): ").lower()
        if use_custom_date == "y":
            y = int(input("Year: "))
            m = int(input("Month: "))
            d = int(input("Day: "))
            checkout_date = date(y, m, d)
        else:
            checkout_date = None
        try:
            library.checkout_book(member_id, isbn, checkout_date)
            print("Book checked out successfully!")
        except Exception as e:
            print("Error:", e)

    elif choice == "4":
        member_id = input("Enter Member ID: ")
        isbn = input("Enter Book ISBN: ")
        use_custom_date = input("Use custom return date? (y/n): ").lower()
        if use_custom_date == "y":
            y = int(input("Year: "))
            m = int(input("Month: "))
            d = int(input("Day: "))
            return_date = date(y, m, d)
        else:
            return_date = None
        try:
            library.return_book(member_id, isbn, return_date)
            print("Book returned successfully!")
        except Exception as e:
            print("Error:", e)

    elif choice == "5":
        member_id = input("Enter Member ID to calculate fine: ")
        try:
            total_fine = library.calculate_fine(member_id)
            print(f"Total Fine for {member_id}: ${total_fine:.2f}")
        except Exception as e:
            print("Error:", e)

    elif choice == "6":
        member_id = input("Enter Member ID to view borrowing history: ")
        try:
            history_member = library._get_member(member_id)
            history = library.get_member_borrowing_history(member_id)
            print(f"\nBorrowing History for {history_member.name}:")
            for b in history:
                print(
                    f"- {b.book.title} | Checkout: {b.checkout_date} | Due: {b.due_date} | Returned: {b.return_date}"
                )
        except Exception as e:
            print("Error:", e)

    elif choice == "7":
        print("Exiting library system. Goodbye!")
        break

    else:
        print("Invalid choice! Please enter a number 1-7.")