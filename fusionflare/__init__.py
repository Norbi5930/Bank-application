from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config.from_object("config")
db.init_app(app)




from fusionflare import routes