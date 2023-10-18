from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, IntegerField, SubmitField, DateField, BooleanField
from wtforms.validators import Length, Email, EqualTo, InputRequired, ValidationError
from datetime import date

from fusionflare.models import User




class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(10, 30)], render_kw={"placeholder": "Felhasználónév"})
    email = EmailField(validators=[InputRequired(), Email()], render_kw={"placeholder": "E-mail"})
    phone_number = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Telefonszám"})
    birth_data = DateField("Születési dátum", validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired(), Length(8)], render_kw={"placeholder": "Jelszó"})
    password_confirm = PasswordField(validators=[InputRequired(), EqualTo("password", message="A két jelszó nem eggyezik!")], render_kw={"placeholder": "Jelszó újra"})
    accept_privacy = BooleanField()
    submit = SubmitField("Regisztráció")


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError(message="Ez a felhasználónév már foglalt!")
        
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError(message="Ez az e-mail cím már használatban van!")

    def validate_birth_data(self, birth_data):
        now_year = date.today().year

        if now_year - birth_data.data.year < 13:
            raise ValidationError(message="Túl fiatal vagy ahhoz, hogy fiókod legyen!")
        if now_year - birth_data.data.year > 99:
            raise ValidationError(message="Érvényes dátumot adj meg!")
    
    def validate_accept_privacy(self, accept_privacy):
        if accept_privacy.data:
            pass
        else:
            raise ValidationError(message="Nem fogadtad el a felhasználási feltételeket!")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Felhasználónév"})
    card_number = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Kártyaszám"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Jelszó"})
    submit = SubmitField("Bejelentkezés")

