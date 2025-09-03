from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False) # Student, Staff, Alumni, Guest
    has_seen_welcome = db.Column(db.Boolean, default=False, nullable=False)

    def get_id(self):
        return str(self.id)
