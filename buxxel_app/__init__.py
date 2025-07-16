from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config.from_pyfile('../config.py')

    db.init_app(app)

    from buxxel_app.auth.routes import auth
    from buxxel_app.marketplace.routes import marketplace
    from buxxel_app.dashboard.routes import dashboard
    from buxxel_app.main.routes import main

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(marketplace)
    app.register_blueprint(dashboard)

    return app
