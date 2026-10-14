import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'bellbird.db')


def get_db():
    """Return a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they do not exist."""
    conn = get_db()
    cursor = conn.cursor()

    # New books: quantity-based, one row per title
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS new_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT,
            quantity INTEGER NOT NULL DEFAULT 1,
            price REAL NOT NULL,
            location TEXT NOT NULL
        )
    ''')

    # Second-hand books: individual records, one row per physical copy
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS second_hand_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            condition TEXT NOT NULL,
            price REAL NOT NULL,
            location TEXT NOT NULL,
            source TEXT,
            paid REAL
        )
    ''')

    # Customers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            contact_preference TEXT DEFAULT 'call'
        )
    ''')

    # Customer orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            book_title TEXT NOT NULL,
            author TEXT,
            quantity INTEGER DEFAULT 1,
            status TEXT DEFAULT 'Ordered',
            ordered_date TEXT,
            arrived_date TEXT,
            picked_up_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')

    conn.commit()
    conn.close()


# --- New Book Operations ---

def add_new_book(title, author, isbn, quantity, price, location):
    conn = get_db()
    conn.execute(
        'INSERT INTO new_books (title, author, isbn, quantity, price, location) VALUES (?, ?, ?, ?, ?, ?)',
        (title, author, isbn, quantity, price, location)
    )
    conn.commit()
    conn.close()


def get_all_new_books():
    conn = get_db()
    rows = conn.execute('SELECT * FROM new_books ORDER BY title').fetchall()
    conn.close()
    return rows


def update_new_book_quantity(book_id, delta):
    conn = get_db()
    conn.execute(
        'UPDATE new_books SET quantity = quantity + ? WHERE id = ?',
        (delta, book_id)
    )
    conn.commit()
    conn.close()


def delete_new_book(book_id):
    conn = get_db()
    conn.execute('DELETE FROM new_books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()


# --- Second-hand Book Operations ---

def add_second_hand_book(title, author, condition, price, location, source, paid):
    conn = get_db()
    conn.execute(
        'INSERT INTO second_hand_books (title, author, condition, price, location, source, paid) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (title, author, condition, price, location, source, paid)
    )
    conn.commit()
    conn.close()


def get_all_second_hand_books():
    conn = get_db()
    rows = conn.execute('SELECT * FROM second_hand_books ORDER BY title').fetchall()
    conn.close()
    return rows


def sell_second_hand_book(book_id):
    """Remove a single second-hand book record. Other copies are unaffected."""
    conn = get_db()
    conn.execute('DELETE FROM second_hand_books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()


def delete_second_hand_book(book_id):
    conn = get_db()
    conn.execute('DELETE FROM second_hand_books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()


# --- Search ---

def search_all_books(query):
    """Search both new and second-hand books by partial title or author."""
    conn = get_db()
    like = f'%{query}%'

    new_rows = conn.execute(
        'SELECT *, "new" AS type FROM new_books WHERE title LIKE ? OR author LIKE ?',
        (like, like)
    ).fetchall()

    sh_rows = conn.execute(
        'SELECT *, "second-hand" AS type FROM second_hand_books WHERE title LIKE ? OR author LIKE ?',
        (like, like)
    ).fetchall()

    conn.close()
    return list(new_rows) + list(sh_rows)


# --- Customer Operations ---

def add_customer(name, contact, preference):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO customers (name, contact, contact_preference) VALUES (?, ?, ?)',
        (name, contact, preference)
    )
    customer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return customer_id


def get_customer_by_name(name):
    conn = get_db()
    row = conn.execute('SELECT * FROM customers WHERE name = ?', (name,)).fetchone()
    conn.close()
    return row


# --- Order Operations ---

def create_order(customer_id, book_title, author, quantity, ordered_date):
    conn = get_db()
    conn.execute(
        'INSERT INTO orders (customer_id, book_title, author, quantity, status, ordered_date) VALUES (?, ?, ?, ?, ?, ?)',
        (customer_id, book_title, author, quantity, 'Ordered', ordered_date)
    )
    conn.commit()
    conn.close()


def get_all_orders():
    conn = get_db()
    rows = conn.execute('''
        SELECT o.*, c.name AS customer_name, c.contact AS customer_contact
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        ORDER BY o.id DESC
    ''').fetchall()
    conn.close()
    return rows


def get_outstanding_orders():
    """Return all orders that have not been picked up yet."""
    conn = get_db()
    rows = conn.execute('''
        SELECT o.*, c.name AS customer_name, c.contact AS customer_contact
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        WHERE o.status NOT IN ('Picked up', 'Cancelled')
        ORDER BY o.id DESC
    ''').fetchall()
    conn.close()
    return rows


def update_order_status(order_id, new_status, date_value):
    """Move order forward through Ordered -> Arrived -> Picked up."""
    conn = get_db()
    if new_status == 'Arrived':
        conn.execute(
            'UPDATE orders SET status = ?, arrived_date = ? WHERE id = ?',
            (new_status, date_value, order_id)
        )
    elif new_status == 'Picked up':
        conn.execute(
            'UPDATE orders SET status = ?, picked_up_date = ? WHERE id = ?',
            (new_status, date_value, order_id)
        )
    else:
        conn.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, order_id))
    conn.commit()
    conn.close()


def search_orders(query):
    """Search orders by customer name or book title."""
    conn = get_db()
    like = f'%{query}%'
    rows = conn.execute('''
        SELECT o.*, c.name AS customer_name, c.contact AS customer_contact
        FROM orders o
        JOIN customers c ON o.customer_id = c.id
        WHERE c.name LIKE ? OR o.book_title LIKE ?
        ORDER BY o.id DESC
    ''', (like, like)).fetchall()
    conn.close()
    return rows


def get_order_by_id(order_id):
    """Retrieve a single order by its ID."""
    conn = get_db()
    row = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    conn.close()
    return row


def update_order(order_id, book_title, author, quantity):
    """Update an existing order's book title, author, and quantity."""
    conn = get_db()
    conn.execute(
        'UPDATE orders SET book_title = ?, author = ?, quantity = ? WHERE id = ?',
        (book_title, author, quantity, order_id)
    )
    conn.commit()
    conn.close()


def cancel_order(order_id):
    """Cancel an order by setting its status to Cancelled."""
    conn = get_db()
    conn.execute("UPDATE orders SET status = 'Cancelled' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()