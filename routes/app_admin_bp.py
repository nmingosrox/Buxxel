# app_admin routes go here

from flask import Blueprint, render_template, flash, redirect, url_for
from models import db, Product

admin_bp = Blueprint('admin_bp', __name__)

@admin_route.route('/')
def admin_dashboard():
    vendors = Vendor.query.order_by(Vendor.username.asc()).all()
    return render_template('admin_dashboard.html', vendors=vendors)


# view all products on the app posted by purveyors
@admin_bp.route('/products')
def admin_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin_products.html', products=products)

# toggle featured purveyors (purveyors that appear on the homepage)
@admin_bp.route('/toggle/<int:vendor_id>')
def toggle_featured(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    vendor.is_featured = not vendor.is_featured
    db.session.commit()                               flash("Vendor featured status updated.", "suc>
    return redirect(url_for('admin_dashboard'))

# delete purveyors from the app
@@admin_bp_route.route('/admin/delete/<int:vendor_id>')
def delete_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    db.session.delete(vendor)
    db.session.commit()
    flash("Vendor deleted.", "danger")
    return redirect(url_for('admin_dashboard'))

