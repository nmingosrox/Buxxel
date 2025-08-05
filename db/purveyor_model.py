from db import db

class Purveyor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(120))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(120))  # filename for profile image
    is_available_for_commissions = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)

