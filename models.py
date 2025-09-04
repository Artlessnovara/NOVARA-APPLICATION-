from flask_login import UserMixin
from app import db
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

# Association Table for User <-> Community many-to-many relationship
community_members = db.Table('community_members',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('community_id', db.Integer, db.ForeignKey('community.id'), primary_key=True)
)

# Association Table for User <-> Project many-to-many relationship (for supporters)
project_supporters = db.Table('project_supporters',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False) # Student, Staff, Alumni, Guest

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    owned_projects = db.relationship('Project', backref='owner', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    stories = db.relationship('Story', backref='author', lazy='dynamic')

    communities = db.relationship('Community', secondary=community_members,
                                  backref=db.backref('members', lazy='dynamic'),
                                  lazy='dynamic')
    supported_projects = db.relationship('Project', secondary=project_supporters,
                                         backref=db.backref('supporters', lazy='dynamic'),
                                         lazy='dynamic')

    def get_id(self):
        return str(self.id)

    def has_liked_post(self, post):
        return Like.query.filter(
            Like.user_id == self.id,
            Like.post_id == post.id).count() > 0

    def is_member(self, community):
        return self.communities.filter(
            community_members.c.community_id == community.id).count() > 0

    def has_supported_project(self, project):
        return self.supported_projects.filter(
            project_supporters.c.project_id == project.id).count() > 0

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expires_sec)
            user_id = data.get('user_id')
        except Exception:
            return None
        return User.query.get(user_id)

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    posts = db.relationship('Post', backref='community', lazy='dynamic')

    def __repr__(self):
        return f'<Community {self.name}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    tagline = db.Column(db.String(250), nullable=True)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Project {self.title}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_content = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=True)
    likes = db.relationship('Like', backref='post', lazy='dynamic')
    media = db.relationship('Media', backref='post', lazy='dynamic', cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Post {self.text_content[:50]}...>'

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media_type = db.Column(db.String(50), nullable=False) # 'image' or 'video'
    file_path = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.text_content[:50]}...>'

class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media_type = db.Column(db.String(50), nullable=False) # 'image' or 'video'
    file_path = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Story {self.id} by User {self.user_id}>'
