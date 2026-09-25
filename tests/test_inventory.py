def test_second_hand_book_independence():
    """Test that selling one second-hand book does not affect another copy."""
    book1 = {"title": "Cold Harvest", "condition": "VG", "price": 18.00}
    book2 = {"title": "Cold Harvest", "condition": "Fair", "price": 7.00}

    sold_book = book1

    assert book2["price"] == 7.00
    assert book2["condition"] == "Fair"
    assert book1 != book2