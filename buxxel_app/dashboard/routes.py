from flask import Blueprint, render_template
from buxxel_app.models import Product

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/seller/<int:user_id>')
def seller_dashboard(user_id):
    products = Product.query.filter_by(owner_id=user_id).all()
    return render_template('seller_dashboard.html', products=products)
