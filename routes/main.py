from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

bp = Blueprint('main', __name__)

from flask_login import login_required, current_user
from app import db

@bp.route('/')
@login_required
def index():
    if not current_user.has_seen_welcome:
        return redirect(url_for('main.welcome'))
    return render_template('index.html')

@bp.route('/welcome')
@login_required
def welcome():
    if current_user.has_seen_welcome:
        return redirect(url_for('main.index'))
    return render_template('welcome.html')

@bp.route('/welcome/complete')
@login_required
def welcome_complete():
    current_user.has_seen_welcome = True
    db.session.commit()
    return redirect(url_for('main.index'))
