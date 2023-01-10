from flask import render_template, url_for, request, redirect, flash
from blog import app, db, mail
from flask_mail import Message
from blog.models import User, Post, Comment
from flask_bootstrap import Bootstrap4
from blog.forms import RegistrationForm, LoginForm, PostForm, SearchForm, CommentForm, ResetRequestForm, ResetPasswordForm
from flask_login import UserMixin, login_user, logout_user, current_user,LoginManager,login_required
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import smtplib
from email.message import EmailMessage
from sqlalchemy import create_engine
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer as Serializer
import uuid as uuid
import os

@app.route('/')
def fl():
    return render_template('index.html')

@app.route("/home",methods=['GET','POST'])
@login_required
def home():        
  users_list = User.query.order_by(User.date)  
  id = current_user.id
  if id == 11:
    return render_template('home.html',users_list=users_list)
  else:
      flash('Only Admin can operate.')
  return redirect(url_for('404'))  

@app.route("/admin")
@login_required
def admin():
  id = current_user.id
  if id == 11:
    return render_template('admin.html')  
  else:
    flash('Only Admin can operate.')
    return redirect(url_for('dashboard'))  

@app.route("/index")
def index():
  posts=Post.query.all()
  return render_template('index.html',posts=posts)  


@app.route("/register",methods=['GET','POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()   
    if user is None:
      user = User(username=form.username.data, email=form.email.data, password=form.password.data)
      db.session.add(user)
      db.session.commit()

      form.username.data = ''
      form.email.data = ''
      form.password.data = ''
      
      flash('Registration successful!')

    if user:
      flash('Email Already Used by Other User')  
          
  users_list = User.query.order_by(User.id)  
  # return redirect(url_for('registered'))
  return render_template('register.html',title='Register',form=form,users_list=users_list)

@app.route("/registered")
def registered():
  return render_template('registered.html', title='Thanks!')

@app.route("/login",methods=['GET','POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user)
      flash('You\'ve successfully logged in,'+' '+ current_user.username +'!')
      return redirect(url_for('dashboard'))
    flash('Invalid username or password.')
  return render_template('login.html',title='Login', form=form)

@app.route("/logout")
def logout():
  logout_user()
  flash('You\'re now logged out. Thanks for your visit!')
  return render_template('logout.html')

@app.route("/reset_password",methods=['GET','POST'])
def reset_request():
  form=ResetRequestForm()
  if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
          send_mail(user)
          flash('Reset request sent. Please check your mail.')
          return redirect(url_for('login'))
        else:
          flash('User does not exist. Please check again!')  
  return render_template('reset_request.html',title='reset request',form=form,legend='Reset Password')


# def send_mail(user):
#     token=user.get_token()
#     msg=Message('Password Reset Request',recipients=[user.email],sender='donoreply@limin.com')
#     msg.body=f'''To reset your password. Please follow the link below.
#     {url_for('reset_token',token=token,_external=True)}
#     If you have recieve email before. Please ignore this message.
#     '''
#     mail.send(msg)

@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_request_token(token):
      user=User.verify_token(token)
      if user is None:
            flash('That is invalid token or expired.Please try again.')
            return redirect('reset_request.html')
      form=ResetPasswordForm()      
      if form.validate_on_submit():
        user = User(password=form.password.data)
        db.session.commit(user)
        flash('Password changed! Please Log in')
        return redirect(url_for('login'))
      return render_template('change_password.html',title='Change Pssword',legend='Change Pssword',form=form)   

@app.route("/dashboard",methods=['GET','POST'])
@login_required
def dashboard():
  return render_template('dashboard.html')

@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
  form = PostForm()
   
  if form.validate_on_submit():
      user = current_user.id
      post = Post(title=form.title.data,content=form.content.data,slug=form.slug.data,author_id = user)
      form.title.data = ''
      form.content.data = ''
      form.slug.data = ''

      db.session.add(post)
      db.session.commit()

      flash('Comment Post Successfully!')
  return render_template('Add_Post.html', form=form)  

@app.route('/posts')
def posts():
  posts = Post.query.order_by(Post.date)
  return render_template('posts.html',posts=posts)  

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
  post=Post.query.get_or_404(post_id)
  return render_template('post.html',title=post.title,post=post)

@app.route("/post/edit/<int:post_id>",methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
      post=Post.query.get_or_404(post_id)
      form = PostForm()
      if form.validate_on_submit():
            post.title = form.title.data
            post.slug = form.slug.data
            post.content = form.content.data
            db.session.add(post)
            db.session.commit()
            flash('Comment Has Been Successfully Updated!')
            return redirect(url_for('post',post_id=post.id))
      if current_user.id == post.author_id:
        form.title.data=post.title
        form.slug.data=post.slug 
        form.content.data=post.content
        return render_template('edit_post.html',form=form)
      else:
        flash('You are not authorized to edit this comment.')  
        posts = Post.query.order_by(Post.date)
        return render_template('posts.html',posts=posts)

@app.route("/post/delete/<int:post_id>")
def delete_post(post_id):
      post_delete = Post.query.get_or_404(post_id)
      id = current_user.id
      if id == post_delete.author_id:
            
        try:
              db.session.delete(post_delete)
              db.session.commit()
              flash('Comment Deleted!')

              posts = Post.query.order_by(Post.date)
              return render_template('posts.html',posts=posts) 
      
        except:
              flash('Some mistakes happened, try again.') 
              posts = Post.query.order_by(Post.date)
              return render_template('posts.html',posts=posts) 
      
      else:
            flash('Only the Poster Can Delete this Comment.')
            posts = Post.query.order_by(Post.date)
            return render_template('posts.html',posts=posts) 
       

@app.route("/user_remove/<int:id>")
def remove_user(id):
      form = RegistrationForm()
      user_to_remove = User.query.get_or_404(id)
      try:
            db.session.delete(user_to_remove)
            db.session.commit()
            flash('User Deleted!')

            users_list = User.query.order_by(User.date) 
            return render_template('home.html',form=form, users_list=users_list) 
     
      except:
            flash('Some mistakes happened, try again.') 
            users_list = User.query.order_by(User.date) 
            return render_template('home.html',form=form, users_list=users_list) 
     
@app.route("/update/<int:id>",methods=['GET', 'POST'])
def update(id):
      form = RegistrationForm()
      user_update = User.query.get_or_404(id)
      if request.method == 'POST':
          user_update.username = request.form['username']
          user_update.email = request.form['email']
          user_update.image_file = request.files['image_file']

          if request.files['image_file']:
            user_update.image_file = request.files['image_file']
                

            pic_filename = secure_filename(user_update.image_file.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            saver = request.files['image_file']
            user_update.image_file = pic_name
            try:
              db.session.commit()
              saver.save(os.path.join(app.config['UPLOAD_FOLDER'],pic_name))
              flash('Profile Updated!') 
              return render_template('update.html',
              form = form, user_update=user_update) 
            except:
              flash('Oops! Something went wrong. Please try again!')
              return render_template('update.html',
              form = form, user_update=user_update)

          else:
              flash('Please upload a pic!')    
              return render_template('update.html',
              form = form, user_update=user_update)
      else:
            return render_template('update.html',
            form = form, user_update=user_update)

@app.route("/search",methods=['GET', 'POST'])
def search():
      form = SearchForm()
      posts = Post.query
      if form.validate_on_submit():
            post.searched = form.searched.data
            posts = posts.filter(Post.content.like('%'+ post.searched + '%'))
            posts = posts.order_by(Post.title).all()
            return render_template('search.html',form=form,searched=post.searched,posts=posts)
      else:
            flash('You do not input search keywords.')
            return render_template('search.html',form=form)

@app.route("/create-comment/<post_id>",methods=['GET','POST'])
def create_comment(post_id):
  text = request.form.get('text')
  if not text:
      flash('Content can not be empty!',category='error')
  else:
    post=Post.query.filter_by(id=post.id)  
    if post:
      comment = Comment(text=text,author_id=current_user.id,post_id=post_id)
      db.session.add(comment)
      db.session.commit()
    else:
      flash('Post does not exist.',category='error')    
  return redirect(url_for("posts"))


@app.context_processor
def base():
      form = SearchForm()
      return dict(form=form)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html')

  

