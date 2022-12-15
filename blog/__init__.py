from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd6fe0e69ea5dfaa765df73887770351883e4c8eb59555e51'
from blog import routes

