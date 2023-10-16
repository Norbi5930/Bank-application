from fusionflare import db, login_manager
from flask_login import UserMixin
from random import randint

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))



class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    card_number = db.Column(db.Integer, nullable=False, unique=True)
    balance = db.Column(db.Integer, nullable=False)
    cvc_code = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    birth_day = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


    def get_id(self):
        return str(self.user_id)