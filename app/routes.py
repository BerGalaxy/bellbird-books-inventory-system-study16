from flask import request, jsonify, Blueprint
from app.models import CustomerOrder 

main = Blueprint('main', __name__)
orders = []

# Feat: MSD426GXUST16-5 add search and filter logic
@main.route('/search')
def search_books():
    query = request.args.get('q', '')
    if not query:
        return {"message": "Please provide a search query"}
    
    # Mock search logic (backend teammate will connect database later)
    matched_books = []
    
    return {"message": f"Searching for: {query}", "results": matched_books}

# --- Story 6: Order Management ---

@main.route('/orders', methods=['POST'])
def create_order():
    """Create a new order with initial status Ordered"""
    data = request.get_json()
    if not data or 'customer_name' not in data or 'book_title' not in data:
        return jsonify({'error': 'Missing customer_name or book_title'}), 400
    
    order = CustomerOrder(data['customer_name'], data['book_title'])
    orders.append(order)
    return jsonify({'message': 'Order created successfully', 'status': order.status}), 201

@main.route('/orders/<int:index>/status', methods=['PUT'])
def update_order_status(index):
    """Update order status: Ordered -> Arrived -> Picked up"""
    if index >= len(orders) or index < 0:
        return jsonify({'error': 'Order not found'}), 404
    
    data = request.get_json()
    new_status = data.get('status')
    allowed_statuses = ['Ordered', 'Arrived', 'Picked up']
    
    if new_status not in allowed_statuses:
        return jsonify({'error': 'Invalid status. Must be one of: Ordered, Arrived, Picked up'}), 400
    
    orders[index].status = new_status
    return jsonify({'message': 'Status updated successfully', 'status': new_status}), 200