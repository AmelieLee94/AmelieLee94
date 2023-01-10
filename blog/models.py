from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from blog import db, login_manager,app
from flask_login import UserMixin, login_user, logout_user, current_user,LoginManager,login_required
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
      return Users.query.get(int(user_id))

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  title = db.Column(db.String(255), nullable=False)
  content = db.Column(db.Text, nullable=False)
  image_file = db.Column(db.String(40), nullable=False, default='default.jpg')
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  slug = db.Column(db.String(255))
  comment = db.relationship('Comment', backref='post', passive_deletes=True, lazy=True)

  def __repr__(self):
    return f"Post('{self.date}', '{self.title}', '{self.content}')"

class Comment(UserMixin,db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  text = db.Column(db.Text,nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

  def get_token(self,expires_sec='300'):
        serial=Serializer(app.config['SECRET_KEY'])
        return serial.dumps({'user_id':user.id}).decode('utf-8')
 
  @staticmethod
  def verify_token(token):
      serial=Serializer(app.config['SECRET_KEY'])
      try:
            user_id=serial.loads(token)['user_id']
      except:
            return None
      return User.query.get(user_id) 

  def __repr__(self):
    return f"User('{self.username}', '{self.email}','{self.password_hash}')"

class User(UserMixin,db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  username = db.Column(db.String(15), unique=True, nullable=False)
  image_file = db.Column(db.String(40), default='default.jpg')
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String(128), nullable=False)
  post = db.relationship('Post', backref='user',passive_deletes=True, lazy=True)
  comment = db.relationship('Comment', backref='user', passive_deletes=True, lazy=True)

#adated from Grinberg(2014, 2018)
  @property
  def password(self):
    raise AttributeError('Password is not readable.')

  @password.setter
  def password(self,password):
    self.password_hash=generate_password_hash(password)

  def verify_password(self,password):
    return check_password_hash(self.password_hash,password)


  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

