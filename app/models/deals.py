from app.models import db

class LightningDeal(db.Model):
    __tablename__ = 'lightning_deals'
    
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    actual_price = db.Column(db.Float)
    final_price = db.Column(db.Float)
    total_units = db.Column(db.Integer)
    available_units = db.Column(db.Integer)
    expiry_time = db.Column(db.DateTime)    
    
    def update(self):
        db.session.commit()

