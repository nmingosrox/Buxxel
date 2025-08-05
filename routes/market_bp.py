# market blueprint routes go here
from flask import Blueprint, render_template, Flask
from db import db, Product

market_bp = Blueprint('market', __name__)

@market_bp.route('/')
def market():
    return 'this is the marketplace'


@market_bp.route('/purveyors_list')
def purveyors_list():
    pass


@market_bp.route('/build_project')
def build_project():
    pass
