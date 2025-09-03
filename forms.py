from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class SignupForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
        ('Student', 'Student'),
        ('Staff', 'Staff'),
        ('Alumni', 'Alumni'),
        ('Guest', 'Guest')
    ], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

from wtforms import TextAreaField
from flask_wtf.file import MultipleFileField, FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

from wtforms.validators import Optional

class PostForm(FlaskForm):
    text_content = TextAreaField("What's on your mind?", validators=[Optional(), Length(min=0, max=500)])
    media = MultipleFileField('Add Photos/Videos', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'mp4', 'mov', 'avi'], 'Images or Videos only!')
    ])
    community = SelectField('Post to Community', coerce=int)
    submit = SubmitField('Post')

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(min=5, max=150)])
    tagline = StringField('Tagline', validators=[DataRequired(), Length(min=10, max=250)])
    description = TextAreaField('Detailed Description', validators=[DataRequired(), Length(min=50)])
    submit = SubmitField('Pitch Project')
