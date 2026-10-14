import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bellbird.db')

def create_tables(conn):
    """Create all required tables if they do not exist."""
    cursor = conn.cursor()

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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            contact_preference TEXT DEFAULT 'call'
        )
    ''')

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


def seed():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Ensure tables exist
    create_tables(conn)

    cursor = conn.cursor()

    # Clean existing data to start fresh
    cursor.execute('DELETE FROM orders')
    cursor.execute('DELETE FROM customers')
    cursor.execute('DELETE FROM second_hand_books')
    cursor.execute('DELETE FROM new_books')

    # 1. Add New Books
    cursor.execute("INSERT INTO new_books (title, author, isbn, quantity, price, location) VALUES (?, ?, ?, ?, ?, ?)",
                   ("The Lantern Keeper", "I. Rand", "9780994117205", 3, 32.99, "FIC"))
    cursor.execute("INSERT INTO new_books (title, author, isbn, quantity, price, location) VALUES (?, ?, ?, ?, ?, ?)",
                   ("Small Mercies at Sea", "D. Tran", "9780994118301", 2, 29.99, "FIC"))
    cursor.execute("INSERT INTO new_books (title, author, isbn, quantity, price, location) VALUES (?, ?, ?, ?, ?, ?)",
                   ("The Quiet Reef", "M. Oyelaran", "9780994119476", 4, 34.99, "FIC"))

    # 2. Add Second-hand Books (same title, different condition/price to test independence)
    cursor.execute("INSERT INTO second_hand_books (title, author, condition, price, location, source, paid) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   ("Cold Harvest", "R. Nakamura", "Very Good", 18.00, "BR-C3", "Petrakis house clearance", 5.00))
    cursor.execute("INSERT INTO second_hand_books (title, author, condition, price, location, source, paid) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   ("Cold Harvest", "R. Nakamura", "Fair", 7.00, "BR-C3", "Petrakis house clearance", 1.00))
    cursor.execute("INSERT INTO second_hand_books (title, author, condition, price, location, source, paid) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   ("Nightjar", "C. Deasy", "As New", 45.00, "under counter", "Petrakis house clearance", 8.00))

    # 3. Add Customers
    cursor.execute("INSERT INTO customers (name, contact, contact_preference) VALUES (?, ?, ?)",
                   ("H. Petrakis", "0412 774 209", "call"))
    cursor.execute("INSERT INTO customers (name, contact, contact_preference) VALUES (?, ?, ?)",
                   ("J. Whelan", "j.whelan@example.com", "email"))

    # 4. Add Orders
    cursor.execute("INSERT INTO orders (customer_id, book_title, author, quantity, status, ordered_date, arrived_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (1, "Ferns of the Southeast", "K. Doull", 1, "Arrived", "2026-07-29", "2026-08-04"))
    cursor.execute("INSERT INTO orders (customer_id, book_title, author, quantity, status, ordered_date, arrived_date, picked_up_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (2, "The Lantern Keeper", "I. Rand", 2, "Picked up", "2026-07-30", "2026-08-04", "2026-08-06"))

    conn.commit()
    conn.close()
    print("Database seeded successfully with Bellbird Books sample data!")


if __name__ == '__main__':
    seed()