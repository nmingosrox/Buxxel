from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from buxxel_app import db
from buxxel_app.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)
        role = request.form['role']

        user = User(email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()

        flash('Signup successful!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')  # Placeholder for now
