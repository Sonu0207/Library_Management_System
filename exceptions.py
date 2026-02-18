class LibraryError(Exception):
    pass

class BookNotFoundError(LibraryError):
    pass

class MemberNotFoundError(LibraryError):
    pass

class CheckoutRuleViolation(LibraryError):
    pass