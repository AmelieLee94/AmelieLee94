from flask import render_template, url_for, request, redirect, flash
from blog import app, db
from blog.models import User, Post, Comment
from flask_bootstrap import Bootstrap4
from blog.forms import RegistrationForm, LoginForm, PostForm, SearchForm, CommentForm
from flask_login import UserMixin, login_user, logout_user, current_user,LoginManager,login_required
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
import smtplib
from sqlalchemy import create_engine
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditor, upload_success, upload_fail
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer as Serializer
import uuid as uuid
import os
from sqlalchemy import desc

@app.route('/')
def fl():
    return render_template('index.html')

@app.route("/home",methods=['GET','POST'])
@login_required
def home():        
  users_list = User.query.order_by(desc(User.date))
  id = current_user.id
  if id == 11:
    return render_template('home.html',users_list=users_list)
  else:
      flash('Only Admin can operate.')
  return render_template('404.html') 

@app.route("/index")
def index():
  posts=Post.query.all()
  return render_template('index.html',posts=posts)  

# Code to register and log in
# Adpated from flask exercise CMT120 / Flask Documentation(1.1x) 
# https://flask-login.readthedocs.io/en/latest/

@app.route("/register",methods=['GET','POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()   
    username = User.query.filter_by(username=form.username.data).first() 
    if user:
      flash('Email Already Used by Other User!')
      return render_template('register.html',title='Register',form=form)
    elif username:
      flash('Username Already Used by Other User!')
      return render_template('register.html',title='Register',form=form)
    elif user is None and username is None:
      user = User(username=form.username.data, email=form.email.data, password=form.password.data)
      db.session.add(user)
      db.session.commit()

      form.username.data = ''
      form.email.data = ''
      form.password.data = ''
      
      flash('Registration successful!')          
      login_user(user)
      flash('You\'ve successfully logged in,'+' '+ current_user.username +'!')
      return redirect(url_for('dashboard'))
  return render_template('register.html',title='Register',form=form)

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
# end of referenced code


# def send_mail(user):
#     token=user.get_token()
#     msg=Message('Password Reset Request',recipients=[user.email],sender='donoreply@limin.com')
#     msg.body=f'''To reset your password. Please follow the link below.
#     {url_for('reset_token',token=token,_external=True)}
#     If you have recieve email before. Please ignore this message.
#     '''
# #     mail.send(msg)

@app.route("/dashboard",methods=['GET','POST'])
@login_required
def dashboard():
  return render_template('dashboard.html')

# Post upload/delete/edit, upload file, and search content
# Adapted from Youtube channel Codemy.com Flask Friday and Flask Documentation(1.1x) and Flask Advanced Usage
# accessed 24-12-2022
# https://www.youtube.com/watch?v=0Qxtt4veJIc&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz
# https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
# https://flask-ckeditor.readthedocs.io/en/latest/plugins.html

@app.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
  form = PostForm()
   
  if form.validate_on_submit():
      user = current_user.id
      post = Post(title=form.title.data,content=form.content.data,author_id = user)
      form.title.data = ''
      form.content.data = ''

      db.session.add(post)
      db.session.commit()

      flash('Comment Post Successfully!')
      return redirect(url_for("posts"))  

  else: 
     return render_template('Add_Post.html', form=form)  

@app.route('/posts')
def posts():
  posts = Post.query.order_by(desc(Post.date))
  return render_template('posts.html',posts=posts)  

@app.route("/post/<int:post_id>")
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
            post.content = form.content.data

            db.session.add(post)
            db.session.commit()
            flash('Comment Has Been Successfully Updated!')
            return redirect(url_for('post',post_id=post.id))
      if current_user.id == post.author_id or current_user.id == 11:
        form.title.data=post.title
        form.content.data=post.content
        return render_template('edit_post.html',form=form)
      else:
        flash('You are not authorized to edit this comment.')  
        posts = Post.query.order_by(desc(Post.date))
        return render_template('posts.html',posts=posts)

@app.route("/post/delete/<int:post_id>")
def delete_post(post_id):
      post_delete = Post.query.get_or_404(post_id)
      id = current_user.id
      if post_delete.comment:
        flash('Can not delete a comment with replies!')
        posts = Post.query.order_by(desc(Post.date))
        return render_template('posts.html',posts=posts)
      else:
        if id == post_delete.author_id or id==11:
            
          try:
                db.session.delete(post_delete)
                db.session.commit()
                flash('Comment Deleted!')

                posts = Post.query.order_by(desc(Post.date))
                return render_template('posts.html',posts=posts) 
        
          except:
                flash('Some mistakes happened, try again.') 
                posts = Post.query.order_by(desc(Post.date))
                return render_template('posts.html',posts=posts) 
      
        else:
              flash('Only the author can delete this comment.')
              posts = Post.query.order_by(desc(Post.date))
              return render_template('posts.html',posts=posts) 
       

@app.route("/user_remove/<int:id>")
def remove_user(id):
      form = RegistrationForm()
      user_to_remove = User.query.get_or_404(id)
      if user_to_remove.comment or user_to_remove.post:
            flash('Can not delete user who has posted content!')
            users_list = User.query.order_by(desc(User.date)) 
            return render_template('home.html',form=form, users_list=users_list)
      else:      
        try:
              db.session.delete(user_to_remove)
              db.session.commit()
              flash('User Account Deleted!')

              users_list = User.query.order_by(desc(User.date)) 
              return render_template('home.html',form=form, users_list=users_list) 
      
        except:
              flash('Some mistakes happened, try again.') 
              users_list = User.query.order_by(desc(User.date)) 
              return render_template('home.html',form=form, users_list=users_list) 
      
@app.route("/update/<int:id>",methods=['GET', 'POST'])
def update(id):
      form = RegistrationForm()
      user_update = User.query.get_or_404(id)
      if request.method == 'POST':
          user_update.username = request.form['username']
          user_update.email = request.form['email']
          # user_update.image_file = request.files['image_file']

          if request.files['image_file']:
            user_update.image_file = request.files['image_file']
                

            pic_filename = secure_filename(user_update.image_file.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            saver = request.files['image_file']
            user_update.image_file = pic_name
            extension = pic_filename.split('.')[-1].lower()
            if extension not in ['jpg', 'gif', 'png', 'jpeg','svg']:
               flash('Image Only!',category='error')
               return render_template('update.html',
                form = form, user_update=user_update)
            else:
              try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'],pic_name))
                flash('Profile Info and Avatar Updated!') 
                return render_template('update.html',
                form = form, user_update=user_update) 
              except:
                flash('Oops! Something went wrong. Please try again!')
                return render_template('update.html',
                form = form, user_update=user_update)

          else:
              user_update.username = request.form['username']
              user_update.email = request.form['email']   
              user_update.image_file = user_update.image_file
              db.session.commit()
              flash('Profile info changed!')
              return render_template('update.html',
              form = form, user_update=user_update)
      else:
            return render_template('update.html',
            form = form, user_update=user_update)

# Adpated from stackoverflow flask upload image file https://stackoverflow.com/questions/50555668/flask-admin-ckeditor-image-upload

@app.route('/files/<path:filename>')
def uploaded_files(filename):
    path = '/the/uploaded/directory'
    return send_from_directory(path, filename)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')  
    # Add more validations here
    extension = f.filename.split('.')[1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg','svg']:  
        return upload_fail(message='Image only!')  
    f.save(os.path.join('/the/uploaded/directory', f.filename))
    url = url_for('uploaded_files', filename=f.filename)
    return upload_success(url=url) 


@app.route("/search",methods=['GET', 'POST'])
def search():
      form = SearchForm()
      posts = Post.query
      if form.validate_on_submit():
            post.searched = form.searched.data
            posts = posts.filter(Post.content.like('%'+ post.searched + '%'))
            posts = posts.order_by(desc(Post.date)).all()
            return render_template('search.html',form=form,searched=post.searched,posts=posts)
      else:
            flash('You do not input search keywords.')
            return render_template('search.html',form=form)

# end of referenced code

# Comment create/delete/
# Adapted from Youtube channel Tech with Tim
# accessed 10-01-2023
# https://www.youtube.com/watch?v=M_OKJnIdYeU

@app.route("/create-comment/<post_id>",methods=['GET','POST'])
@login_required
def create_comment(post_id):
  text = request.form.get('text')
  if not text:
      flash('Content can not be empty!',category='error')
  else: 
      post=Post.query.filter_by(id=post_id)
      if post: 
        comment = Comment(text=text,author_id=current_user.id,post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('New Reply Added!')
      else:
        flash('Post does not exist.',category='error')    
  return redirect(url_for("posts"))

@app.route("/delete-comment/<comment_id>",methods=['GET','POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if current_user.id != comment.author_id and current_user.id !=comment.post.author_id and current_user.id !=11:
          flash('Only who commented/replied can delete their own content!')
    elif not comment:
          flash('Reply does not exist anymore.')
    else:
         db.session.delete(comment)
         db.session.commit() 
         flash('Reply deleted!')
    return redirect(url_for("posts"))
# end of referenced code

@app.context_processor
def base():
      form = SearchForm()
      return dict(form=form)

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html')

  

