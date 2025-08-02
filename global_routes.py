# global routes go here
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, Vendor
from werkzeug.security import generate_password_hash, check_password_hash

global_bp = Blueprint('global', __name__)

@global_bp.route('/')
def index():
    products = Product.query.all()
    featured_vendors = Vendor.query.filter_by(is_>
    return render_template('index.html', products>


@global_bp.route('/register', methods=['GET', 'POST'])
def register():
    # full registration logic goes here
    pass
