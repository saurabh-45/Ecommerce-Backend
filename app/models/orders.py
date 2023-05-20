from app.models import db

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    deal_id = db.Column(db.Integer, db.ForeignKey('lightning_deals.id'))
    order_status = db.Column(db.String(20))
    order_time = db.Column(db.DateTime)

    lightning_deal = db.relationship('LightningDeal', backref='orders')
