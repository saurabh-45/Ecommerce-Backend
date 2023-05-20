from flask import Blueprint, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from app.models import LightningDeal, Order
from app import db
from datetime import datetime, timedelta

admin_blueprint = Blueprint('admin_blueprint', __name__)

def refresh_lightning_deals():
    # Retrieve all lightning deals from the database
    deals = LightningDeal.query.all()

    for deal in deals:
        # Reset the final price to the actual price
        deal.final_price = deal.actual_price
        deal.update()
            
scheduler = BackgroundScheduler()
scheduler.configure(timezone=utc)
# Start the scheduler
scheduler.start()

# Set the refresh_lightning_deals function to be executed every day at 00:00 UTC
scheduler.add_job(refresh_lightning_deals, 'cron', hour=0, minute=0)



@admin_blueprint.route('/lightning_deals', methods=['POST'])
def create_lightning_deal():
    
    data = request.json
    
    # Extract data from the request
    product_name = data.get('product_name')
    actual_price = data.get('actual_price')
    final_price = data.get('final_price')
    total_units = data.get('total_units')
    expiry_time = data.get('expiry_time')
    
    # Check if the expiry time is within the allowed range (not more than 12 hours)
    now = datetime.utcnow()
    max_expiry_time = now + timedelta(hours=12)
    expiry_time = datetime.fromisoformat(expiry_time)
    
    if expiry_time > max_expiry_time:
        return jsonify({'error': 'Expiry time cannot be more than 12 hours from now'}), 400

    # Create a new lightning deal
    deal = LightningDeal(
        product_name=product_name,
        actual_price=actual_price,
        final_price=final_price,
        total_units=total_units,
        available_units=total_units,
        expiry_time=expiry_time
    )

    # Add the deal to the database
    db.session.add(deal)
    db.session.commit()

    return jsonify({'message': 'Lightning deal created successfully'})

@admin_blueprint.route('/lightning_deals/<int:deal_id>', methods=['PUT'])
def update_lightning_deal(deal_id):
    deal = LightningDeal.query.get(deal_id)
    
    if not deal:
        return jsonify({'error': 'Lightning deal not found'}), 404
    
    data = request.json

    # Update the deal attributes if they are present in the request data
    if 'product_name' in data:
        deal.product_name = data['product_name']
    if 'actual_price' in data:
        deal.actual_price = data['actual_price']
    if 'final_price' in data:
        deal.final_price = data['final_price']
    if 'total_units' in data:
        deal.total_units = data['total_units']
        # If the total units are updated, also update the available units
        deal.available_units = data['total_units']
    if 'expiry_time' in data:
        deal.expiry_time = data['expiry_time']
        expiry_time = datetime.fromisoformat(data['expiry_time'])

        # Check if the expiry time is within the allowed range (not more than 12 hours)
        now = datetime.utcnow()
        max_expiry_time = now + timedelta(hours=12)
        if expiry_time > max_expiry_time:
            return jsonify({'error': 'Expiry time cannot be more than 12 hours from now'}), 400

        deal.expiry_time = expiry_time

    db.session.commit()

    return jsonify({'message': 'Lightning deal updated successfully'})

@admin_blueprint.route('/orders/<int:order_id>/approve', methods=['PUT'])
def approve_order(order_id):
    # Retrieve the order from the database
    order = Order.query.get(order_id)

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    # Update the order status to 'approved'
    order.order_status = 'approved'
    db.session.commit()

    return jsonify({'message': 'Order approved successfully'})
