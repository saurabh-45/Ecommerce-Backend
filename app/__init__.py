from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.routes import *
from flask_mysqldb import MySQLdb
 

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:admin@localhost/deals"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    db.app = app
    migrate = Migrate(app, db)
    app.register_blueprint(admin_blueprint, url_prefix = '/admin')
    app.register_blueprint(customer_blueprint, url_prefix  = '/user')
    
    return app