from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_

from app import db
from models import User, Post, Like
from forms import PostForm

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    if not current_user.has_seen_welcome:
        return redirect(url_for('main.welcome'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Home', posts=posts)

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

@bp.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(text_content=form.text_content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Post', form=form)

@bp.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post.id).first()

    if like:
        # User has already liked the post, so unlike it
        db.session.delete(like)
        db.session.commit()
        liked = False
    else:
        # User has not liked the post, so like it
        like = Like(user_id=current_user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        liked = True

    return jsonify({'success': True, 'likes_count': post.likes.count(), 'liked': liked})
