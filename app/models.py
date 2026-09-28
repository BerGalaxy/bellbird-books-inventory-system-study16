# Data models for Bellbird Books inventory system

class Book:
    """Represents a book in inventory (new or second-hand)."""
    def __init__(self, title, author, condition=None, price=None, quantity=1):
        self.title = title
        self.author = author
        self.condition = condition  # For second-hand books
        self.price = price
        self.quantity = quantity    # For new books


class CustomerOrder:
    """Represents a customer order."""
    def __init__(self, customer_name, book_title, status="Ordered"):
        self.customer_name = customer_name
        self.book_title = book_title
        self.status = status  # Ordered -> Arrived -> Picked up