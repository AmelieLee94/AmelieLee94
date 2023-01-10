from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_mail import Mail


def create_app():
    app = Flask(__name__)

app = Flask(__name__) 

ckeditor = CKEditor(app)

app.config['SECRET_KEY'] = 'd6fe0e69ea5dfaa765df73887770351883e4c8eb59555e51'

# suppress SQLAlchemy warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB Connection changed to mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c22094835:Li12345678@csmysql.cs.cf.ac.uk:3306/c22094835_database1'

UPLOAD_FOLDER = './blog/static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db = SQLAlchemy(app)
bootstrap4 = Bootstrap4(app)
login_manager = LoginManager()
login_manager.init_app(app)

# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT']=587
# app.config['MAIL_USE_TLS']= True
# app.config['MAIL_USERNAME']='limin@gmail.com'
# app.config['MAIL_PASSWORD']='temppassword123!'

mail=Mail(app)

from blog import routes
