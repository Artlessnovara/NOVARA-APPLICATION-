from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from sqlalchemy import or_

from app import db
from models import User

bp = Blueprint('main', __name__)

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

@bp.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('q', '')
    active_tab = request.args.get('tab', 'all')
    people_results = []

    # In the future, this will handle different tabs and result types.
    # For now, 'all' and 'people' will both search for users.
    if query:
        search_term = f"%{query}%"
        if active_tab in ['all', 'people']:
            people_results = User.query.filter(
                or_(
                    User.full_name.ilike(search_term),
                    User.email.ilike(search_term)
                )
            ).all()

    return render_template(
        'search.html',
        query=query,
        people_results=people_results,
        active_tab=active_tab
    )
