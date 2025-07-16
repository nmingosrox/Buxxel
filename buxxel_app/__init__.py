from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db.init_app(app)

    from .auth.routes import auth
    from .marketplace.routes import marketplace
    from .dashboard.routes import dashboard

    app.register_blueprint(auth)
    app.register_blueprint(marketplace)
    app.register_blueprint(dashboard)

    return app
