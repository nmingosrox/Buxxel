from flask_sqlalchemy import SQLAlchemy

# 🔗 Create the SQLAlchemy instance
db = SQLAlchemy()

# 📦 Import model classes
from .purveyor import Purveyor
from .product import Product
# Add other models as needed, e.g. from .build import Build
