from db import db
from datetime import datetime

class Order(db.Model):
    #add client_identifier for backrouting of purveyor to them
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    purveyor_id = db.Column(db.Integer, db.ForeignKey('purveyor.id'))
    quantity = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ProjectBuild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('purveyor.id'))

    # Many-to-many with Purveyors
    purveyors = db.relationship('Purveyor', secondary='project_purveyor', backref='projects')

    # Many-to-many with Products
    products = db.relationship('Product', secondary='project_product', backref='projects')

    status = db.Column(db.String(20), default='draft')  # draft, published
    preview_image = db.Column(db.String(120)) # optional

project_talent = db.Table('project_purveyor',
    db.Column('project_id', db.Integer, db.ForeignKey('project_build.id')),
    db.Column('purveyor_id', db.Integer, db.ForeignKey('purveyor.id'))
)

project_product = db.Table('project_product',
    db.Column('project_id', db.Integer, db.ForeignKey('project_build.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)
