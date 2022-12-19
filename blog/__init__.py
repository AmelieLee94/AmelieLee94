from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'd6fe0e69ea5dfaa765df73887770351883e4c8eb59555e51'

# suppress SQLAlchemy warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB Connection changed to mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c22094835:Li12345678@csmysql.cs.cf.ac.uk:3306/c22094835_database1'

# EXAMPLE:
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c123456:MySQLPassword@csmysql.cs.cf.ac.uk:3306/my_blog_db'
# WHERE:
# 'c123456' is your username (Student Number with leading 'c');
# 'MySQLPassword' is your MySQL password, NOT your University password! These two passwords SHOULD be different for security reasons. Use https://dbmanager.cs.cf.ac.uk/ to manage your passwords
# 'my_blog_db' is the name of your MySQL database

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from blog import routes
