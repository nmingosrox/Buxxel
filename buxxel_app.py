from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from models import db, Product, Vendor, Order, Talent
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from config import DevelopmentConfig, ProductionConfig

def create_app():
    # 🔐 Load environment variables from .env
    load_dotenv()

    # 🔧 Create Flask app instance
    app = Flask(__name__
   
    # load config based on environment (prod/dev)
    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # 🔗 Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # 🔗 Register Blueprints
    app.register_blueprint(global_bp)
    app.register_blueprint(purveyor_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(admin_bp)

    # 🛡️ Optionally setup login manager, mail, or custom error handlers her

    # create db
    with app.app_context():
        db.create_all()

    return app




if __name__ == '__main__':
    app.run(debug=True)
