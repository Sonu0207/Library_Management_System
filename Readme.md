# Library Book Checkout System

---

## Features

- Add books to the library
- Register library members
- Checkout books with rules:
  - Max 3 books per member
  - Books due 14 days from checkout
  - Fines of $0.50 per overdue day
  - Members with unpaid fines > $10 cannot borrow
- Return books
- Calculate member's fines
- View available books
- View borrowing history
- View checked-out books along with the **member ID** who borrowed them

---

## Setup Instructions

1. **Clone the repository** (or download the files):

```
cd library-system
```

2. Run the main program (No external dependencies required):
```
python main.py
```
3. {Optional} Run unit tests:
```
python -m unittest test_library.py
```

## Business Rules

1. Members can borrow **a maximum of 3 books** at a time.
2. Books are due **14 days from checkout**.
3. Overdue books incur a **$0.50/day fine**.
4. Members with **unpaid fines > $10** cannot borrow new books.

---

## Screenshots
1. Launch Screen
![Launch Screen](https://github.com/uptime-crew-recruiting/Sonu0207-repo-7f92e288-88df-4103-960a-92c3ecd7576d/blob/main/library_system/Sample_Images/launchScreen.png)

2. Member Checks out book
![After Checking Out](https://github.com/uptime-crew-recruiting/Sonu0207-repo-7f92e288-88df-4103-960a-92c3ecd7576d/blob/main/library_system/Sample_Images/afterChecout.png)

3. Late Fee Applied
![LateFee](https://github.com/uptime-crew-recruiting/Sonu0207-repo-7f92e288-88df-4103-960a-92c3ecd7576d/blob/main/library_system/Sample_Images/lateFee.png)

4. View Browsing History of Member
![Browsing History](https://github.com/uptime-crew-recruiting/Sonu0207-repo-7f92e288-88df-4103-960a-92c3ecd7576d/blob/main/library_system/Sample_Images/browsingHistory.png)

## Exceptions

- BookNotFoundError – Raised if book does not exist
- MemberNotFoundError – Raised if member does not exist
- CheckoutRuleViolation – Raised if checkout rules are violate
 (e.g. Return Date is later than checkout date, Member checking out more than 3 books, unpaid dues > $10)