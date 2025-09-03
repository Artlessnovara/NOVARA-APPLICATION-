import os
from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from app import db
from models import User, Post, Like, Community, Project, Media, Comment, Story, CreativeWork, Certificate
from forms import PostForm, ProjectForm, StoryForm, CreativeWorkForm, CertificateForm

bp = Blueprint('main', __name__)

@bp.route('/profile/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('profile.html', title=f"{user.full_name}'s Profile", user=user, posts=posts, active_nav='profile')

@bp.route('/user/<int:user_id>/toggle_follow', methods=['POST'])
@login_required
def toggle_follow(user_id):
    user_to_follow = User.query.get_or_404(user_id)
    if user_to_follow == current_user:
        return jsonify({'success': False, 'message': 'You cannot follow yourself.'}), 400

    if current_user.is_following(user_to_follow):
        current_user.unfollow(user_to_follow)
        db.session.commit()
        is_following = False
    else:
        current_user.follow(user_to_follow)
        db.session.commit()
        is_following = True

    return jsonify({
        'success': True,
        'is_following': is_following,
        'followers_count': user_to_follow.followers.count()
    })

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
    query = request.args.get('q', '').strip()
    active_tab = request.args.get('tab', 'all')

    people_results = []
    post_results = []
    community_results = []

    if query:
        search_term = f"%{query}%"

        # Search People
        people_results = User.query.filter(
            or_(
                User.full_name.ilike(search_term),
                User.email.ilike(search_term)
            )
        ).limit(10).all()

        # Search Posts
        post_results = Post.query.filter(
            Post.text_content.ilike(search_term)
        ).order_by(Post.timestamp.desc()).limit(10).all()

        # Search Communities
        community_results = Community.query.filter(
            Community.name.ilike(search_term)
        ).limit(10).all()

    return render_template(
        'search.html',
        query=query,
        people_results=people_results,
        post_results=post_results,
        community_results=community_results,
        active_tab=active_tab,
        active_nav='search'
    )

def get_media_type(filename):
    image_exts = ['jpg', 'jpeg', 'png', 'gif']
    video_exts = ['mp4', 'mov', 'avi']
    ext = filename.split('.')[-1].lower()
    if ext in image_exts:
        return 'image'
    elif ext in video_exts:
        return 'video'
    return None

@bp.route('/create-post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    # Populate the choices for the community dropdown
    form.community.choices = [(c.id, c.name) for c in current_user.communities.order_by('name')]
    form.community.choices.insert(0, (0, 'Main Feed (No Community)'))

    if form.validate_on_submit():
        # Check for empty submission
        if not form.text_content.data and not form.media.data:
            flash('You must provide either text or a media file.', 'warning')
            return render_template('create_post.html', title='New Post', form=form)

        community_id = form.community.data
        post = Post(text_content=form.text_content.data,
                    author=current_user,
                    community_id=community_id if community_id != 0 else None)
        db.session.add(post)
        db.session.flush() # Use flush to get the post ID before committing

        # Handle file uploads
        upload_folder = os.path.join(os.getcwd(), 'static/uploads')

        for file in form.media.data:
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)

                media_type = get_media_type(filename)
                if not media_type:
                    # This should ideally not happen due to form validation, but as a safeguard:
                    continue

                # Store a path relative to the static folder for URL generation
                db_file_path = os.path.join('uploads', filename)

                new_media = Media(media_type=media_type,
                                  file_path=db_file_path,
                                  post_id=post.id)
                db.session.add(new_media)

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

@bp.route('/post/<int:post_id>/toggle_bookmark', methods=['POST'])
@login_required
def toggle_bookmark(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.has_bookmarked_post(post):
        current_user.unbookmark_post(post)
        db.session.commit()
        bookmarked = False
    else:
        current_user.bookmark_post(post)
        db.session.commit()
        bookmarked = True
    return jsonify({'success': True, 'bookmarked': bookmarked})

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

@bp.route('/comments/<int:post_id>', methods=['GET'])
@login_required
def get_comments(post_id):
    post = Post.query.get_or_404(post_id)
    comments = []
    for comment in post.comments.order_by(Comment.timestamp.asc()).all():
        comments.append({
            'id': comment.id,
            'text_content': comment.text_content,
            'timestamp': comment.timestamp.strftime('%b %d, %Y at %I:%M %p'),
            'author': {
                'id': comment.author.id,
                'full_name': comment.author.full_name
            }
        })
    return jsonify(comments)

@bp.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()
    if not data or not data.get('text_content'):
        return jsonify({'error': 'Comment text is required.'}), 400

    comment = Comment(
        text_content=data['text_content'],
        author=current_user,
        post_id=post.id
    )
    db.session.add(comment)
    db.session.commit()

    return jsonify({
        'id': comment.id,
        'text_content': comment.text_content,
        'timestamp': comment.timestamp.strftime('%b %d, %Y at %I:%M %p'),
        'author': {
            'id': comment.author.id,
            'full_name': comment.author.full_name
        }
    }), 201

@bp.route('/story/create', methods=['GET', 'POST'])
@login_required
def create_story():
    form = StoryForm()
    if form.validate_on_submit():
        file = form.media.data
        filename = secure_filename(file.filename)
        upload_folder = os.path.join(os.getcwd(), 'static/uploads/stories')
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        media_type = get_media_type(filename)
        db_file_path = os.path.join('uploads/stories', filename)

        new_story = Story(
            media_type=media_type,
            file_path=db_file_path,
            author=current_user
        )
        db.session.add(new_story)
        db.session.commit()
        flash('Your story has been posted!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create_story.html', title='Create Story', form=form)

@bp.route('/creativity')
@login_required
def creativity_hub():
    works = CreativeWork.query.order_by(CreativeWork.timestamp.desc()).all()
    return render_template('creativity_hub.html', title='Creativity Hub',
                           works=works, active_nav='creativity')

@bp.route('/creativity/upload', methods=['GET', 'POST'])
@login_required
def upload_creative_work():
    form = CreativeWorkForm()
    if form.validate_on_submit():
        file = form.media.data
        filename = secure_filename(file.filename)

        upload_folder = os.path.join(os.getcwd(), 'static/uploads/creative')
        os.makedirs(upload_folder, exist_ok=True) # Ensure the folder exists
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        db_file_path = os.path.join('uploads/creative', filename)

        new_work = CreativeWork(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            file_path=db_file_path,
            author=current_user
        )
        db.session.add(new_work)
        db.session.commit()
        flash('Your creative work has been shared!', 'success')
        return redirect(url_for('main.creativity_hub'))

    return render_template('create_creative_work.html', title='Share Your Work', form=form)

@bp.route('/certificate/add', methods=['GET', 'POST'])
@login_required
def add_certificate():
    form = CertificateForm()
    if form.validate_on_submit():
        file = form.certificate_file.data
        filename = secure_filename(file.filename)

        upload_folder = os.path.join(os.getcwd(), 'static/uploads/certificates')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        db_file_path = os.path.join('uploads/certificates', filename)

        new_cert = Certificate(
            title=form.title.data,
            issuing_organization=form.issuing_organization.data,
            date_issued=form.date_issued.data,
            file_path=db_file_path,
            user=current_user
        )
        db.session.add(new_cert)
        db.session.commit()
        flash('Your certificate has been added!', 'success')
        return redirect(url_for('main.profile', user_id=current_user.id))

    return render_template('add_certificate.html', title='Add Certificate', form=form)

@bp.route('/api/stories')
@login_required
def get_stories():
    twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)
    stories = Story.query.filter(Story.timestamp > twenty_four_hours_ago).order_by(Story.timestamp.desc()).all()

    stories_by_user = {}
    for story in stories:
        user_id = story.author.id
        if user_id not in stories_by_user:
            stories_by_user[user_id] = {
                'user_id': user_id,
                'user_full_name': story.author.full_name,
                'user_avatar': 'https://via.placeholder.com/60', # Placeholder avatar
                'stories': []
            }
        stories_by_user[user_id]['stories'].append({
            'id': story.id,
            'file_path': url_for('static', filename=story.file_path),
            'media_type': story.media_type,
            'timestamp': story.timestamp.isoformat()
        })

    return jsonify(list(stories_by_user.values()))
