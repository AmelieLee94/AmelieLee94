from flask import Flask
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app)

# Adpated from flask exercise CMT120  
app.config['SECRET_KEY'] = 'd6fe0e69ea5dfaa765df73887770351883e4c8eb59555e51'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c22094835:Li12345678@csmysql.cs.cf.ac.uk:3306/c22094835_database1'

# Adpated from Flask Documentation(1.1.x)
UPLOAD_FOLDER = './blog/static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# Adpated from stackoverflow flask upload image file https://stackoverflow.com/questions/50555668/flask-admin-ckeditor-image-upload
app.config['CKEDITOR_SERVE_LOCAL'] = False
app.config['CKEDITOR_HEIGHT'] = 400
app.config['CKEDITOR_FILE_UPLOADER'] = 'upload'
basedir = './blog/upload/'
app.config['UPLOADED_PATH'] = os.path.join(basedir, 'uploads')

# app.config.update(
#     SESSION_COOKIE_SECURE=True,
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE='Lax',
# )


# app.config.update(
#     PERMANENT_SESSION_LIFETIME=600
# )

ckeditor = CKEditor(app)
db = SQLAlchemy(app)
Bootstrap4(app)
login_manager = LoginManager()
login_manager.init_app(app)
csrf = CSRFProtect(app)
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT']=587
# app.config['MAIL_USE_TLS']= True
# app.config['MAIL_USERNAME']='limin@gmail.com'
# app.config['MAIL_PASSWORD']='temppassword123!'

from blog import routes
