from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flaskr.extensions import db

csrf = CSRFProtect()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'
app.config['WTF_CSRF_ENABLED'] = False
csrf.init_app(app)
db.init_app(app)

import flaskr.routes