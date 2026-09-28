from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/inventory')
def inventory():
    return "Inventory page"

@main.route('/orders')
def orders():
    return "Orders page"