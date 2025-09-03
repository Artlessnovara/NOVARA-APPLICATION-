from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_

from app import db
from models import User, Post, Like, Community, Project
from forms import PostForm, ProjectForm

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    if not current_user.has_seen_welcome:
        return redirect(url_for('main.welcome'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Home', posts=posts, active_nav='home')

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
        active_tab=active_tab,
        active_nav='search' # Although there is no search icon in bottom nav, good practice
    )

@bp.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    # Populate the choices for the community dropdown
    form.community.choices = [(c.id, c.name) for c in current_user.communities.order_by('name')]
    form.community.choices.insert(0, (0, 'Main Feed (No Community)'))

    if form.validate_on_submit():
        community_id = form.community.data
        post = Post(text_content=form.text_content.data,
                    author=current_user,
                    community_id=community_id if community_id != 0 else None)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        # Redirect to the community page if posted there, otherwise to the main feed
        if community_id != 0:
            return redirect(url_for('main.community_page', community_id=community_id))
        return redirect(url_for('main.index'))
    return render_template('create_post.html', title='New Post', form=form)

@bp.route('/communities')
@login_required
def communities():
    all_communities = Community.query.order_by(Community.name).all()
    my_communities = current_user.communities.order_by(Community.name).all()
    return render_template('communities_hub.html', title='Communities',
                           all_communities=all_communities,
                           my_communities=my_communities,
                           active_nav='communities')

@bp.route('/community/<int:community_id>')
@login_required
def community_page(community_id):
    community = Community.query.get_or_404(community_id)
    posts = community.posts.order_by(Post.timestamp.desc()).all()
    return render_template('community_page.html', title=community.name, community=community, posts=posts)

@bp.route('/community/<int:community_id>/toggle_join', methods=['POST'])
@login_required
def toggle_join(community_id):
    community = Community.query.get_or_404(community_id)
    if current_user.is_member(community):
        current_user.communities.remove(community)
        db.session.commit()
        is_member = False
    else:
        current_user.communities.append(community)
        db.session.commit()
        is_member = True

    return jsonify({
        'success': True,
        'is_member': is_member,
        'member_count': community.members.count()
    })

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

@bp.route('/project/<int:project_id>/toggle_support', methods=['POST'])
@login_required
def toggle_support(project_id):
    project = Project.query.get_or_404(project_id)
    if current_user.has_supported_project(project):
        current_user.supported_projects.remove(project)
        db.session.commit()
        is_supporter = False
    else:
        current_user.supported_projects.append(project)
        db.session.commit()
        is_supporter = True

    return jsonify({
        'success': True,
        'is_supporter': is_supporter,
        'supporter_count': project.supporters.count()
    })

@bp.route('/create-project', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(title=form.title.data,
                          tagline=form.tagline.data,
                          description=form.description.data,
                          owner=current_user)
        db.session.add(project)
        db.session.commit()
        flash('Your project has been created and is now live!', 'success')
        return redirect(url_for('main.index')) # Redirect to home page for now
    return render_template('create_project.html', title='Pitch a New Project', form=form)

@bp.route('/innovation')
@login_required
def innovation_hub():
    projects = Project.query.order_by(Project.timestamp.desc()).all()
    return render_template('innovation_hub.html', title='Innovation Hub',
                           projects=projects, active_nav='innovation')
