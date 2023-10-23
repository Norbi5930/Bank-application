from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from random import randint, sample

from fusionflare import app, db, bcrypt
from fusionflare.forms import RegisterForm, LoginForm, SecurityForm, PasswordChangeForm
from fusionflare.models import User
from fusionflare.email_sender import SuccesRegister, NewLogin, PasswordChange




with app.app_context():
    db.create_all()
    db.session.commit()



@app.route("/")
def home():
    return render_template("index.html", title="Főoldal")



@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if form.validate_on_submit():
        try:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            card_number = generate_card_number()
            cvc_code = generate_cvc_code()
            user = User(username=form.username.data, card_number=card_number, balance=0, cvc_code=cvc_code, email=form.email.data, birth_day=form.birth_data.data, phone_number=form.phone_number.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            SuccesRegister(form.username.data, card_number, form.email.data).send_email()
            flash("Sikeres regisztráció!", "succes")
        except:
            flash("Sikertelen regisztráció, próbáld újra később.", "danger")

        return redirect(url_for("home"))

    return render_template("register.html", title="Regisztráció", form=form)


def generate_card_number():
    while True:
            unique_card_number = "".join([str(randint(0, 9)) for _ in range(12)])
            if not User.query.filter_by(card_number=unique_card_number).first():
                card_number = unique_card_number
                print(card_number)
                break
    
    return card_number


def generate_cvc_code():
    code = "".join([str(randint(0, 9)) for _ in range(3)])


    return code



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if form.validate_on_submit():
        cleaned_card_number = form.card_number.data.replace("-", "")
        user = User.query.filter_by(username=form.username.data, card_number=cleaned_card_number).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            flash("Sikeres bejelentkezés!", "succes")
            NewLogin(current_user.username, current_user.email).send_email()
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Sikertelen bejelentkezés, ellenőrizze a felhasználónevét, kártyaszámát vagy jelszavát!", "danger")

    return render_template("login.html", title="Bejelentkezés", form=form)


@app.route("/information", methods=["GET", "POST"])
@login_required
def information():
    if request.method == "POST":
        if security():
            number = 0
            card_number = ""
            for numbers in str(current_user.card_number):
                if number == 4:
                    card_number += "-"
                    number = 0
                number += 1
                card_number += numbers

            return render_template("information.html", title="Információk", card_number=card_number)
        else:
            logout_user()
            flash("Mivel nem tudtad magad igazolni, ezért kizártunk a rendszerből!", "danger")
            return redirect(url_for("home"))
    else:
        form = SecurityForm()
        return render_template("security.html", form=form, title = "Ellenőrzés")

def security():
    form = SecurityForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            return True
        
    return False



@app.route("/new_password", methods=["GET", "POST"])
def new_password_request():

    if request.method == "POST":
        
        link = generate_link()

        PasswordChange(current_user.username, current_user.email, f"http://localhost:5000/new_password/{link}/{current_user.user_id}").send_email()

        flash("A szükséges emailt elküldtük!", "succes")

        return redirect(url_for("home"))


    return render_template("new_password_request.html", title="Jelszóváltás")


def generate_link():
    
    character = "qwertzuiopasdfghjklyxcvbnm123456789"
    size = 16

    link = "".join(sample(character, size))

    return link


@app.route(f"/new_password/<link>/<id>", methods=["GET", "POST"])
def new_password(link,id):
    form = PasswordChangeForm()
    user = User.query.get_or_404(id)

    if form.validate_on_submit():
        if bcrypt.check_password_hash(user.password, form.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode("utf-8")
            user.password = hashed_password
            db.session.commit()
            logout_user()
            flash("Sikeres jelszó váltás!", "succes")
            return redirect(url_for("home"))
        else:
            logout_user()
            flash("Helytelen jelszó! Ki lettél dobva a rendszerből!", "danger")
            return redirect(url_for("home"))

    return render_template("new_password.html", title="Jelszóváltás", form=form)



@app.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html", title="Privacy")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sikeres kijelentkezés!", "succes")
    return redirect(url_for("home"))