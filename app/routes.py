from flask import request

# Feat: MSD426GXUST16-5 add search and filter logic
@app.route('/search')
def search_books():
    query = request.args.get('q', '')
    if not query:
        return {"message": "Please provide a search query"}
    
    # 模拟搜索逻辑（后续由后端队友连接数据库）
    matched_books = []
    
    return {"message": f"Searching for: {query}", "results": matched_books}
# --- Story 6: Order Management ---

@main.route('/orders', methods=['POST'])
def create_order():
    """创建新订单，初始状态为 Ordered"""
    data = request.get_json()
    if not data or 'customer_name' not in data or 'book_title' not in data:
        return jsonify({'error': 'Missing customer_name or book_title'}), 400
    
    order = CustomerOrder(data['customer_name'], data['book_title'])
    orders.append(order)
    return jsonify({'message': 'Order created successfully', 'status': order.status}), 201

@main.route('/orders/<int:index>/status', methods=['PUT'])
def update_order_status(index):
    """更新订单状态：Ordered -> Arrived -> Picked up"""
    if index >= len(orders) or index < 0:
        return jsonify({'error': 'Order not found'}), 404
    
    data = request.get_json()
    new_status = data.get('status')
    allowed_statuses = ['Ordered', 'Arrived', 'Picked up']
    
    if new_status not in allowed_statuses:
        return jsonify({'error': 'Invalid status. Must be one of: Ordered, Arrived, Picked up'}), 400
    
    orders[index].status = new_status
    return jsonify({'message': 'Status updated successfully', 'status': new_status}), 200