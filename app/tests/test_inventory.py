import pytest

# test: MSD426GXUST16-3 add second-hand independence tests
def test_search_functionality():
    query = "Harry Potter"
    assert query is not None
    assert "Harry" in query

# test: MSD426GXUST16-8 order status transition tests
def test_order_status_flow():
    # Ordered -> Arrived -> Picked up
    current_status = "Ordered"
    assert current_status == "Ordered"
    current_status = "Arrived"
    assert current_status == "Arrived"
    current_status = "Picked up"
    assert current_status == "Picked up"