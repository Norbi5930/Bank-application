from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from random import randint

from fusionflare import app, db, bcrypt
from fusionflare.forms import RegisterForm, LoginForm
from fusionflare.models import User




with app.app_context():
    db.create_all()
    db.session.commit()



@app.route("/")
def home():
    return render_template("index.html", title="Főoldal")



@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, card_number=generate_card_number(), balance=0, cvc_code=generate_cvc_code(), email=form.email.data, birth_day=form.birth_data.data, phone_number=form.phone_number.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Sikeres regisztráció!", "succes")
        return redirect(url_for("home"))

    return render_template("register.html", title="Regisztráció", form=form)


def generate_card_number():
    while True:
            unique_card_number = "".join([str(randint(0, 9)) for _ in range(12)])
            if not User.query.filter_by(card_number=unique_card_number).first():
                card_number = unique_card_number
                break
    
    return int(card_number)


def generate_cvc_code():
    code = "".join([str(randint(0, 9)) for _ in range(3)])


    return int(code)



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            flash("Sikeres bejelentkezés!", "succes")
            print(current_user.card_number)
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Sikertelen bejelentkezés, ellenőrizze a felhasználónevet vagy a jelszót!", "danger")

    return render_template("login.html", title="Bejelentkezés", form=form)



@app.route("/information", methods=["GET", "POST"])
def information():
    return render_template("information.html", title="Információk")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sikeres kijelentkezés!", "succes")
    return redirect(url_for("home"))