from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Hashed
    is_verified = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(120))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(120))  # filename of avatar image
    is_available_for_commissions = db.Column(db.Boolean, default=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)  # Changed from String to Float for numeric queries
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(120))

    category = db.Column(db.String(50))  # Optional: useful for filtering
    is_published = db.Column(db.Boolean, default=True)  # Controls visibility in marketplace
    is_featured = db.Column(db.Boolean, default=False)  # For homepage highlights

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    vendor = db.relationship('Vendor', backref='products')

    def __repr__(self):
        return f'<Product {self.name}>'


    def __repr__(self):
        return f'<Product {self.name}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))
    quantity = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
