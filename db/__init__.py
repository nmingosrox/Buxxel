from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Lazy imports — models can access this without redefining db
from db.purveyor_model import Purveyor
from db.product_model import Product
from db.market_model import Order
