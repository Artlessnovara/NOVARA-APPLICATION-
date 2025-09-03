from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from forms import LoginForm, SignupForm
from app import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data,
            has_seen_welcome=False
        )
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully signed up! Please login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/signup.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid email or password')
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
