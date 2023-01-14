from flask_wtf import FlaskForm
from wtforms import StringField, FileField,PasswordField, SubmitField, SelectField, BooleanField,EmailField
from wtforms.validators import InputRequired, Email, DataRequired, EqualTo, ValidationError, Length, Regexp
from blog.models import User
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_ckeditor import CKEditorField

class RegistrationForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired(),Regexp('^[0-9A-Za-z]{4,8}$',message='Your username should be 4-8 characters long, and can not contain symbols.')])
  email = EmailField('Email Address', validators=[DataRequired(), Email()])
  password = PasswordField('Password',validators=[DataRequired(),EqualTo('password_confirm',message='Passwords Must Match!'),Length(min=8, max=80)])
  password_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
  image_file = FileField('Profile')
  submit = SubmitField('Submit')
  
  # def validate_username(self, username):
  #   user = User.query.filter_by(username=username.data).first()
  #   if user is not None:
  #     raise ValidationError('Username already exist. Please choose a different one.')

  
  def validate_password(self, password):
    user = User.query.filter_by(password=password.data).first()
    if user is not None:
      raise ValidationError('Password not match.')

class LoginForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired(),Length(min=4, max=15)])
  password = PasswordField('Password',validators=[DataRequired(),Length(min=8, max=80)])
  remember = BooleanField('remember me')
  submit = SubmitField('Login')

# class ResetRequestForm(FlaskForm):
#   username = StringField('Username',validators=[DataRequired(),Length(min=4, max=15)])    
#   key = StringField('Key',validators=[DataRequired()])    
#   email = EmailField('Email Address', validators=[DataRequired(), Email()])
#   submit = SubmitField('Sumbit')  

# class ResetPasswordForm(FlaskForm):
#   password = PasswordField('Password',validators=[DataRequired(),EqualTo('password_confirm',message='Passwords Must Match!'),Length(min=8, max=80)])
#   password_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
#   submit = SubmitField('Submit')  

class PostForm(FlaskForm):
  title = StringField('Title',validators=[DataRequired()])
  content = CKEditorField('Content',validators=[DataRequired()])
  submit = SubmitField('Submit')

class CommentForm(FlaskForm):
  text = StringField('text',validators=[DataRequired()])
  submit = SubmitField('Comment')

class SearchForm(FlaskForm):   
  searched = StringField('Searched',validators=[DataRequired()])
  submit = SubmitField('Submit')
