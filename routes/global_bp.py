# global blueprint routes go here

from flask import Blueprint, render_template
from db import Vendor  # assuming you moved models to /db

global_bp = Blueprint('global_bp', __name__)

@global_bp.route('/')
def index():
    featured_vendors = Vendor.query.filter_by(is_featured=True).limit(6).all()
    return render_template('index.html', featured_vendors=featured_vendors)

