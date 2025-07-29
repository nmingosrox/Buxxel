from flask import Flask, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from models import db, Product, Vendor, Order, Talent
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import flask_profiler

app = Flask(__name__)

app.config["flask_profiler"] = {
    "enabled": app.config["DEBUG"],
    "storage": {
        "engine": "sqlite"
    },
    "basicAuth": {
        "enabled": True,
        "username": "admin",
        "password": "admin"
    },
    "ignore": ["^/static/.*"]
}

# Configuration
app.secret_key = 'your_secret_key_here'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the folder exists

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///buxxel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
migrate = Migrate(app, db)


flask_profiler.init_app(app)

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'vendor_id' not in session:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_file = request.files.get('image')  # 🔧 Define safely

        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)

            new_product = Product(
                name=name,
                price=price,
                description=description,
                image=f'images/{filename}',
                vendor_id=session['vendor_id']
            )
            db.session.add(new_product)
            db.session.commit()

        return redirect(url_for('dashboard'))

    # Handle search query (GET)
    query = request.args.get('q')
    if query:
        try:
            products = Product.query.filter(
                Product.vendor_id == session['vendor_id'],
                Product.name.ilike(f'%{query}%')
            ).all()
        except Exception as e:
            print("Dashboard query error:", e)
            products = []
    else:
        products = Product.query.filter_by(vendor_id=session['vendor_id']).all()

    return render_template('dashboard.html', products=products)

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id, vendor_id=session['vendor_id']).first_or_404()

    # Delete image file if it exists
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(product.image))
    if os.path.exists(image_path):
        os.remove(image_path)

    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/vendors')
def vendors():
    vendors = vendors = Vendor.query.all()
    return render_template('vendors.html', vendors=vendors)

@app.route('/skills')
def skills():
    talents = Talent.query.order_by(Talent.name.asc()).all()
    return render_template('skills_talent.html', talents=talents)

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.filter_by(id=product_id, vendor_id=session['vendor_id']).first_or_404()

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.description = request.form['description']

        image_file = request.files['image']
        if image_file and image_file.filename != '':
            # Delete old image
            old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(product.image))
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

            # Save new image
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            product.image = f'images/{filename}'

        db.session.commit()
        return redirect(url_for('dashboard'))

    return render_template('edit_product.html', product=product)

from flask import jsonify

@app.route('/search')
def live_search():
    query = request.args.get('q', '')
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    rendered = render_template('_product_card.html', products=products)
    return jsonify({'html': rendered})

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('term', '')
    suggestions = Product.query.filter(Product.name.ilike(f'%{query}%')).limit(10).all()
    return jsonify([product.name for product in suggestions])



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        existing_vendor = Vendor.query.filter_by(username=username).first()

        if existing_vendor:
            flash("Username already exists. Please choose a different one.")
            return redirect(url_for('register'))

        password = generate_password_hash(request.form['password'])
        vendor = Vendor(username=username, password=password)
        db.session.add(vendor)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        vendor = Vendor.query.filter_by(username=request.form['username']).first()
        if vendor and check_password_hash(vendor.password, request.form['password']):
            session['vendor_id'] = vendor.id
            session['vendor_username'] = vendor.username
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('vendor_id', None)
    session.pop('vendor_username', None)
    flash('You’ve been logged out.')
    return redirect(url_for('index'))

@app.route('/market')
def market():
    query = request.args.get('query')
    category = request.args.get('category')
    price = request.args.get('price')

    # Start with all published products
    products_query = Product.query.filter_by(is_published=True)

    # Apply filters only if they exist
    if query:
        products_query = products_query.filter(Product.name.ilike(f"%{query}%"))
    if category:
        products_query = products_query.filter_by(category=category)
    if price == "low":
        products_query = products_query.filter(Product.price < 50)
    elif price == "med":
        products_query = products_query.filter(Product.price.between(50, 200))
    elif price == "high":
        products_query = products_query.filter(Product.price > 200)

    products = Product.query.all()
    return render_template("market.html", products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("product_detail.html", product=product)

@app.route('/vendor/<int:vendor_id>')
def vendor_profile(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    vendor_products = Product.query.filter_by(vendor_id=vendor.id).all()
    total_sales = Order.query.filter_by(vendor_id=vendor.id).count()

    # Optional: calculate stats
    total_products = len(vendor_products)
    avg_price = round(sum([p.price for p in vendor_products]) / total_products, 2) if total_products else 0

    return render_template('vendor_profile.html',
                           vendor=vendor,
                           products=vendor_products,
                           total_products=total_products,
                           avg_price=avg_price)

@app.route('/vendors')
def vendor_directory():
    query = request.args.get('q', '')
    if query:
        vendors = Vendor.query.filter(Vendor.username.ilike(f"%{query}%")).all()
    else:
        vendors = Vendor.query.all()
    return render_template('vendor_directory.html', vendors=vendors, query=query)

@app.route('/vendor/settings', methods=['GET', 'POST'])
def vendor_settings():
    vendor_id = session.get('vendor_id')
    if not vendor_id:
        return redirect(url_for('login'))

    vendor = Vendor.query.get_or_404(vendor_id)

    if request.method == 'POST':
        vendor.location = request.form.get('location')
        vendor.bio = request.form.get('bio')
        vendor.is_available_for_commissions = bool(request.form.get('is_available_for_commissions'))


        # Handle avatar upload
        avatar_file = request.files.get('avatar')
        if avatar_file and avatar_file.filename:
            filename = secure_filename(avatar_file.filename)
            avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], 'vendor_avatars', filename)
            avatar_file.save(avatar_path)
            vendor.avatar = filename

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('vendor_settings'))

    return render_template("vendor_settings.html", vendor=vendor)

@app.route('/build')
def build_project():
    all_talents = Talent.query.all()
    all_products = Product.query.all()
    return render_template('build.html', talents=all_talents, products=all_products)

@app.route('/build', methods=['POST'])
def submit_project():
    title = request.form.get('title')
    description = request.form.get('description')
    talent_ids = request.form.getlist('talents')
    product_ids = request.form.getlist('products')
    
    project = ProjectBuild(title=title, description=description, creator_id=session['user_id'])
    project.talents = Talent.query.filter(Talent.id.in_(talent_ids)).all()
    project.products = Product.query.filter(Product.id.in_(product_ids)).all()

    db.session.add(project)
    db.session.commit()
    flash("Project created successfully!", "success")
    return redirect(url_for('dashboard'))

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
