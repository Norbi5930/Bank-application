from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Api

db = SQLAlchemy()
app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
api = Api(app)
app.config.from_object("config")
db.init_app(app)


login_manager.login_message = "Ezt az oldalt csak bejelentkezett személyek érhetik el!"
login_manager.login_message_category = "danger"
login_manager.login_view = "login"



from fusionflare import routes

from fusionflare.bank_api import BankAPI
api.add_resource(BankAPI, '/api/bank/<int:card_number>')