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

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    text_content = TextAreaField("What's on your mind?", validators=[DataRequired(), Length(min=1, max=500)])
    community = SelectField('Post to Community', coerce=int)
    submit = SubmitField('Post')
