class Book:
    def __init__(self, title, author, is_second_hand=False):
        self.title = title
        self.author = author
        self.is_second_hand = is_second_hand

class CustomerOrder:
    def __init__(self, customer_name, book_title):
        self.customer_name = customer_name
        self.book_title = book_title
        self.status = "Ordered"  # 初始状态