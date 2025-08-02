class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(120))

    category = db.Column(db.String(50))  # Option>
    is_published = db.Column(db.Boolean, default=>
    is_featured = db.Column(db.Boolean, default=F>

    vendor_id = db.Column(db.Integer, db.ForeignK>
    vendor = db.relationship('Vendor', backref='p>
    created_at = db.Column(db.DateTime, default=d>

    def __repr__(self):
        return f'<Product {self.name}>'
