from datetime import date
from flask import request, jsonify, Blueprint, render_template, redirect, url_for, flash
from app.models import (
    add_new_book, get_all_new_books, update_new_book_quantity, delete_new_book,
    add_second_hand_book, get_all_second_hand_books, sell_second_hand_book, delete_second_hand_book,
    search_all_books,
    add_customer, get_customer_by_name,
    create_order, get_all_orders, get_outstanding_orders, update_order_status, search_orders,
    get_order_by_id, update_order, cancel_order
)

main = Blueprint('main', __name__)


# --- Page Routes ---

@main.route('/')
def index():
    """Home page: combined inventory dashboard."""
    new_books = get_all_new_books()
    sh_books = get_all_second_hand_books()
    return render_template('index.html', new_books=new_books, sh_books=sh_books)


@main.route('/search')
def search_page():
    """Search results page for inventory."""
    query = request.args.get('q', '').strip()
    results = search_all_books(query) if query else []
    return render_template('search.html', query=query, results=results)


@main.route('/books/new/add', methods=['GET', 'POST'])
def add_new_book_page():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        isbn = request.form.get('isbn', '').strip()
        quantity = request.form.get('quantity', '1')
        price = request.form.get('price', '0')
        location = request.form.get('location', '').strip()

        if not title or not author or not location:
            flash('Title, author, and location are required.', 'error')
            return redirect(url_for('main.add_new_book_page'))

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            flash('Invalid number format for quantity or price.', 'error')
            return redirect(url_for('main.add_new_book_page'))

        add_new_book(title, author, isbn, quantity, price, location)
        flash(f'Added "{title}" to new book stock.', 'success')
        return redirect(url_for('main.index'))

    return render_template('add_new_book.html')


@main.route('/books/second-hand/add', methods=['GET', 'POST'])
def add_second_hand_book_page():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        condition = request.form.get('condition', 'Good')
        price = request.form.get('price', '0')
        location = request.form.get('location', '').strip()
        source = request.form.get('source', '').strip()
        paid = request.form.get('paid', '0')

        if not title or not author or not location:
            flash('Title, author, and location are required.', 'error')
            return redirect(url_for('main.add_second_hand_book_page'))

        try:
            price = float(price)
            paid = float(paid)
        except ValueError:
            flash('Invalid number format for price or paid amount.', 'error')
            return redirect(url_for('main.add_second_hand_book_page'))

        add_second_hand_book(title, author, condition, price, location, source, paid)
        flash(f'Added second-hand copy of "{title}" ({condition}).', 'success')
        return redirect(url_for('main.index'))

    return render_template('add_second_hand_book.html')


@main.route('/books/new/<int:book_id>/sell', methods=['POST'])
def sell_new_book(book_id):
    """Decrease quantity by 1 when a new book is sold."""
    update_new_book_quantity(book_id, -1)
    flash('Quantity decreased by 1.', 'success')
    return redirect(url_for('main.index'))


@main.route('/books/new/<int:book_id>/restock', methods=['POST'])
def restock_new_book(book_id):
    """Increase quantity by 1 for a restock."""
    update_new_book_quantity(book_id, 1)
    flash('Quantity increased by 1.', 'success')
    return redirect(url_for('main.index'))


@main.route('/books/second-hand/<int:book_id>/sell', methods=['POST'])
def sell_second_hand(book_id):
    """Remove a single second-hand book record."""
    sell_second_hand_book(book_id)
    flash('Second-hand copy sold and removed.', 'success')
    return redirect(url_for('main.index'))


# --- Orders ---

@main.route('/orders')
def orders_page():
    """Order list page with search."""
    query = request.args.get('q', '').strip()
    if query:
        orders = search_orders(query)
    else:
        orders = get_all_orders()
    return render_template('orders.html', orders=orders, query=query)


@main.route('/orders/new', methods=['GET', 'POST'])
def new_order_page():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        contact = request.form.get('contact', '').strip()
        preference = request.form.get('preference', 'call')
        book_title = request.form.get('book_title', '').strip()
        author = request.form.get('author', '').strip()
        quantity = request.form.get('quantity', '1')

        if not customer_name or not contact or not book_title:
            flash('Customer name, contact, and book title are required.', 'error')
            return redirect(url_for('main.new_order_page'))

        try:
            quantity = int(quantity)
        except ValueError:
            flash('Quantity must be a valid number.', 'error')
            return redirect(url_for('main.new_order_page'))

        customer = get_customer_by_name(customer_name)
        if customer is None:
            customer_id = add_customer(customer_name, contact, preference)
        else:
            customer_id = customer['id']

        create_order(customer_id, book_title, author, quantity, str(date.today()))
        flash(f'Order created for {customer_name}.', 'success')
        return redirect(url_for('main.orders_page'))

    return render_template('add_order.html')


@main.route('/orders/<int:order_id>/edit', methods=['GET', 'POST'])
def edit_order_page(order_id):
    """Edit an existing customer order."""
    order = get_order_by_id(order_id)
    if order is None:
        flash('Order not found.', 'error')
        return redirect(url_for('main.orders_page'))

    if request.method == 'POST':
        book_title = request.form.get('book_title', '').strip()
        author = request.form.get('author', '').strip()
        quantity = request.form.get('quantity', '1')

        if not book_title:
            flash('Book title is required.', 'error')
            return redirect(url_for('main.edit_order_page', order_id=order_id))

        try:
            quantity = int(quantity)
        except ValueError:
            flash('Quantity must be a valid number.', 'error')
            return redirect(url_for('main.edit_order_page', order_id=order_id))

        update_order(order_id, book_title, author, quantity)
        flash('Order updated successfully.', 'success')
        return redirect(url_for('main.orders_page'))

    return render_template('edit_order.html', order=order)


@main.route('/orders/<int:order_id>/cancel', methods=['POST'])
def cancel_order_page(order_id):
    """Cancel a customer order."""
    cancel_order(order_id)
    flash('Order cancelled.', 'success')
    return redirect(url_for('main.orders_page'))


@main.route('/orders/<int:order_id>/status', methods=['POST'])
def update_status(order_id):
    new_status = request.form.get('status')
    if new_status not in ['Ordered', 'Arrived', 'Picked up']:
        flash('Invalid status.', 'error')
        return redirect(url_for('main.orders_page'))

    update_order_status(order_id, new_status, str(date.today()))
    flash(f'Order #{order_id} updated to {new_status}.', 'success')
    return redirect(url_for('main.orders_page'))


@main.route('/orders/outstanding')
def outstanding_orders_page():
    orders = get_outstanding_orders()
    return render_template('orders.html', orders=orders, query='Outstanding only')


# --- JSON API (kept for backward compatibility) ---

@main.route('/api/search')
def api_search_books():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"message": "Please provide a search query"}), 400
    results = [dict(row) for row in search_all_books(query)]
    return jsonify({"query": query, "results": results})


@main.route('/api/orders', methods=['POST'])
def api_create_order():
    data = request.get_json()
    if not data or 'customer_name' not in data or 'book_title' not in data:
        return jsonify({'error': 'Missing customer_name or book_title'}), 400

    customer = get_customer_by_name(data['customer_name'])
    if customer is None:
        customer_id = add_customer(data['customer_name'], data.get('contact', 'unknown'), 'call')
    else:
        customer_id = customer['id']

    create_order(customer_id, data['book_title'], data.get('author', ''), 1, str(date.today()))
    return jsonify({'message': 'Order created successfully', 'status': 'Ordered'}), 201