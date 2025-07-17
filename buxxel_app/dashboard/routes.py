from flask import Blueprint, render_template
from buxxel_app.models import Product
from buxxel_app.models import User

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route("/seller/<int:seller_id>")
def seller_dashboard(seller_id):
    user = User.query.get_or_404(seller_id)
    return render_template("seller_dashboard.html", user=user)
