from flask import Blueprint, render_template, Flask
from db import db, Product

purveyor_bp = Blueprint('purveyor', __name__)

# purveyor blueprint routes go here
@purveyor_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # ensure user is logged in as a purveyor
    if 'vendor_id' not in session:
        flash('Please log in...')
        return redirect(url_for('global_bp.login'))

    if request.method == 'POST':
        # collect form details for adding a product
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        image_file = request.files.get('image')

        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
#            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#            image_file.save(image_path)
#
#            new_product = Product(name=name,
#                price=price,
#                description=description,
#                image=f'images/{filename}',
#                vendor_id=session['vendor_id']
#                    )
#            db.session.add(new_product)
#            db.session.commit()
#            flash('product added successfully')
#            return redirect(url_for('purveyor_bp.dashboard')

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



@purveyor_bp.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.filter_by(id=product_id, vendor_id=session['vendor_id']).first_or_404()

    # Delete image file if it exists
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(product.image))
    if os.path.exists(image_path):
        os.remove(image_path)

    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('dashboard'))

@purveyor_bp.route('/edit/<int:product_id>', methods=['GET', 'POST'])
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


@purveyor_bp.route('/logout')
def logout():
    session.pop('vendor_id', None)
    session.pop('vendor_username', None)
    flash('You’ve been logged out.')
    return redirect(url_for('index'))



@purveyor_bp.route('/vendor/<int:vendor_id>')
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


@purveyor_bp.route('/vendor/settings', methods=['GET', 'POST'])
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
