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
    is_featured = db.Column(db.Boolean, default=False)


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


class Talent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(120))
    category = db.Column(db.String(50))
    featured_work = db.Column(db.String(120))

class ProjectBuild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('vendor.id'))

    # Many-to-many with Talents
    talents = db.relationship('Talent', secondary='project_talent', backref='projects')

    # Many-to-many with Products
    products = db.relationship('Product', secondary='project_product', backref='projects')

    status = db.Column(db.String(20), default='draft')  # draft, published
    preview_image = db.Column(db.String(120))

project_talent = db.Table('project_talent',
    db.Column('project_id', db.Integer, db.ForeignKey('project_build.id')),
    db.Column('talent_id', db.Integer, db.ForeignKey('talent.id'))
)

project_product = db.Table('project_product',
    db.Column('project_id', db.Integer, db.ForeignKey('project_build.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)
