from flask import Blueprint, render_template, request, redirect, url_for, flash
from buxxel_app import db
from buxxel_app.models import Product

marketplace = Blueprint('marketplace', __name__, url_prefix='/marketplace')

@marketplace.route('/list', methods=['GET', 'POST'])
def list_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        owner_id = 1  # 🔐 Replace with session logic later

        product = Product(name=name, description=description, price=price, owner_id=owner_id)
        db.session.add(product)
        db.session.commit()

        flash('Product listed!', 'success')
        return redirect(url_for('marketplace.view_products'))

    return render_template('list_product.html')

@marketplace.route('/view')
def view_products():
    products = Product.query.all()
    return render_template('view_products.html', products=products)
