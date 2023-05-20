from flask import Blueprint, jsonify, request
from app.models import LightningDeal, Order
from app import db
from datetime import datetime

customer_blueprint = Blueprint('customer_blueprint', __name__)


@customer_blueprint.route('/lightning_deals', methods=['GET'])
def get_available_deals():
    # Retrieve all unexpired lightning deals from the database
    deals = LightningDeal.query.filter(LightningDeal.expiry_time > datetime.utcnow()).all()

    # Prepare the response data
    response = []
    for deal in deals:
        response.append({
            'id': deal.id,
            'product_name': deal.product_name,
            'actual_price': deal.actual_price,
            'final_price': deal.final_price,
            'total_units': deal.total_units,
            'available_units': deal.available_units,
            'expiry_time': deal.expiry_time
        })

    return jsonify(response)

@customer_blueprint.route('/orders', methods=['POST'])
def place_order():
    data = request.json

    # Extract data from the request
    customer_name = data.get('customer_name')
    deal_id = data.get('deal_id')

    # Retrieve the lightning deal associated with the order
    deal = LightningDeal.query.get(deal_id)

    if not deal:
        return jsonify({'error': 'Lightning deal not found'}), 404

    # Check if the deal has expired
    if deal.expiry_time < datetime.utcnow():
        return jsonify({'error': 'The lightning deal has expired'}), 400

    # Check if there are available units for the deal
    if deal.available_units == 0:
        return jsonify({'error': 'No available units for the lightning deal'}), 400

    # Create a new order
    order = Order(
        customer_name=customer_name,
        deal_id=deal_id,
        order_status='pending',
        order_time=datetime.utcnow()
    )

    # Update the available units for the lightning deal
    deal.available_units -= 1

    # Add the order and update the deal in the database
    db.session.add(order)
    db.session.commit()

    return jsonify({'message': 'Order placed successfully'})

@customer_blueprint.route('/orders/<int:order_id>', methods=['GET'])
def check_order_status(order_id):
    # Retrieve the order from the database
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    # Prepare the response data
    response = {
        'id': order.id,
        'customer_name': order.customer_name,
        'deal_id': order.deal_id,
        'order_status': order.order_status,
        'order_time': order.order_time
    }

    return jsonify(response)
