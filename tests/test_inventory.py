import os
import tempfile
import pytest
from app import create_app
from app import models
from app.models import (
    init_db, add_new_book, get_all_new_books, update_new_book_quantity,
    add_second_hand_book, get_all_second_hand_books, sell_second_hand_book,
    add_customer, create_order, get_all_orders, update_order_status, search_all_books
)

@pytest.fixture(autouse=True)
def setup_test_db():
    """Create a temporary test database for each test run."""
    fd, temp_path = tempfile.mkstemp()
    original_path = models.DB_PATH
    models.DB_PATH = temp_path
    
    app = create_app()
    with app.app_context():
        init_db()
    yield app
    
    os.close(fd)
    os.remove(temp_path)
    models.DB_PATH = original_path

@pytest.fixture
def client(setup_test_db):
    return setup_test_db.test_client()

def test_second_hand_independence():
    """Verify that selling one second-hand copy leaves the other copy untouched."""
    add_second_hand_book("Cold Harvest", "R. Nakamura", "Fair", 7.00, "BR-C3", "Petrakis", 1.00)
    add_second_hand_book("Cold Harvest", "R. Nakamura", "Very Good", 18.00, "BR-C3", "Petrakis", 5.00)

    books = get_all_second_hand_books()
    cold_harvest_copies = [b for b in books if b['title'] == "Cold Harvest"]
    assert len(cold_harvest_copies) == 2

    fair_copy = [b for b in cold_harvest_copies if b['condition'] == 'Fair'][0]
    sell_second_hand_book(fair_copy['id'])

    updated_books = get_all_second_hand_books()
    vg_copy = [b for b in updated_books if b['condition'] == 'Very Good']
    assert len(vg_copy) == 1
    assert vg_copy[0]['price'] == 18.00

def test_new_book_quantity_logic():
    """Verify that new books are managed by quantity."""
    add_new_book("The Lantern Keeper", "I. Rand", "123", 3, 32.99, "FIC")
    books = get_all_new_books()
    book = [b for b in books if b['title'] == "The Lantern Keeper"][0]
    assert book['quantity'] == 3

    update_new_book_quantity(book['id'], -1)
    updated_book = [b for b in get_all_new_books() if b['title'] == "The Lantern Keeper"][0]
    assert updated_book['quantity'] == 2

def test_order_status_transition():
    """Verify order status flow: Ordered -> Arrived -> Picked up."""
    customer_id = add_customer("Priya", "12345", "call")
    create_order(customer_id, "The Quiet Reef", "M. Oyelaran", 1, "2026-10-14")

    orders = get_all_orders()
    assert len(orders) == 1
    assert orders[0]['status'] == 'Ordered'

    update_order_status(orders[0]['id'], 'Arrived', '2026-10-15')
    assert get_all_orders()[0]['status'] == 'Arrived'

    update_order_status(orders[0]['id'], 'Picked up', '2026-10-16')
    assert get_all_orders()[0]['status'] == 'Picked up'

def test_search_functionality():
    """Verify partial title/author search works."""
    add_new_book("Nightjar", "C. Deasy", "123", 1, 45.00, "BR-A1")
    results = search_all_books("Night")
    assert len(results) == 1
    assert results[0]['title'] == "Nightjar"

    results_author = search_all_books("Dea")
    assert len(results_author) == 1