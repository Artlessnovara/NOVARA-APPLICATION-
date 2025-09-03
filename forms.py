from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField
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
from flask_wtf.file import FileField, MultipleFileField, FileAllowed

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

class StoryForm(FlaskForm):
    media = FileField('Upload Image or Video', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'mp4', 'mov', 'avi'], 'Images or Videos only!')
    ])
    submit = SubmitField('Post Story')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class CreativeWorkForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    category = SelectField('Category', choices=[
        ('Art', 'Art'),
        ('Music', 'Music'),
        ('Writing', 'Writing'),
        ('Stage', 'Stage')
    ], validators=[DataRequired()])
    media = FileField('Upload Your Work', validators=[
        DataRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'mp3', 'wav', 'pdf', 'txt'], 'Allowed files are images, audio, or documents.')
    ])
    submit = SubmitField('Share Work')

class CertificateForm(FlaskForm):
    title = StringField('Certificate Title', validators=[DataRequired(), Length(max=150)])
    issuing_organization = StringField('Issuing Organization', validators=[DataRequired(), Length(max=150)])
    date_issued = DateField('Date Issued (YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    certificate_file = FileField('Upload Certificate File', validators=[
        DataRequired(),
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg'], 'PDF or Image files only!')
    ])
    submit = SubmitField('Add Certificate')
