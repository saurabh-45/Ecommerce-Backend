from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .deals import LightningDeal
from .orders import Order
