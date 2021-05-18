from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

# ! LOGIN
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # ! Filtering user with this email
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect Password, Try again', category='error')
        else:
            flash('No account created, Create one now', category='error')
            return redirect(url_for('auth.sign_up'))

    return render_template("login.html", user=current_user)

# ! LOGOUT
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# ! SIGN UP
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        blood_type = request.form.get('blood_type')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        mylist = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')
        elif len(email) < 3:
            flash('Invalid Email', category='error')
        elif len(name) < 2:
            flash('Name must be at least of 1 character', category='error')
        elif len(phone) < 11:
            flash('Invalid Phone Number', category='error')
        elif len(phone) > 11:
            flash('Invalid Phone Number', category='error')
        elif blood_type.upper() not in mylist:
            flash("Enter Valid Blood Type", category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            # ? ADD USER TO DATABASE
            new_user = User(email = email,
                            name = name,
                            phone = phone,
                            blood_type = blood_type,
                            gender = gender,
                            password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created', category="success")
            
            return redirect(url_for('views.dashboard'))

    return render_template("sign_up.html", user= current_user)
