# global blueprint routes go here

from flask import Blueprint, render_template
from db import Purveyor  # assuming you moved models to /db

global_bp = Blueprint('global_bp', __name__)

@global_bp.route('/')
def index():
    featured_purveyors = Purveyor.query.filter_by(is_featured=True).limit(6).all()
    return render_template('index.html', featured_purveyors=featured_purveyors)


@global_bp.route('/login')
def login():
    pass


@global_bp.route('/register')
def register():
    pass
