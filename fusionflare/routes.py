from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from random import randint, sample

from fusionflare import app, db, bcrypt
from fusionflare.forms import RegisterForm, LoginForm, SecurityForm, PasswordChangeForm, TransferForm
from fusionflare.models import User
from fusionflare.email_sender import SuccesRegister, NewLogin, PasswordChange, SuccesTransaction




with app.app_context():
    db.create_all()
    #hashed = bcrypt.generate_password_hash("Csipsz123").decode("utf-8")
    #user = User(username="Norbi", card_number="123456789000", balance=50, cvc_code="000", email="bnorbert0925@gmail.com", birth_day="2009-01-26", phone_number="+380123456789", password=hashed)
    #db.session.add(user)
    #hashed = bcrypt.generate_password_hash("Csipsz123").decode("utf-8")
    #user = User(username="Jancsika", card_number="123456789001", balance=50, cvc_code="000", email="bnorbert@gmail.com", birth_day="2009-02-26", phone_number="+380123456784", password=hashed)
    #db.session.add(user)
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
            user = User(username=form.username.data, card_number=card_number, balance=50, cvc_code=cvc_code, email=form.email.data, birth_day=form.birth_data.data, phone_number=form.phone_number.data, password=hashed_password)
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
            if not User.query.filter_by(card_number=unique_card_number).first() and unique_card_number[0] != 0:
                card_number = unique_card_number
                break
    
    return card_number


def generate_cvc_code():
    while True:
        code = "".join([str(randint(0, 9)) for _ in range(3)])

        if code[0] != 0:
            break

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
    form = SecurityForm()
    if request.method == "POST":
        if security(form.password.data):
            number = 0
            card_number = ""
            for numbers in str(current_user.card_number):
                if number == 4:
                    card_number += "-"
                    number = 0
                number += 1
                card_number += numbers
            print(type(current_user.cvc_code))
            return render_template("information.html", title="Információk", card_number=card_number, cvc_code=str(current_user.cvc_code))
        else:
            logout_user()
            flash("Mivel nem tudtad magad igazolni, ezért kizártunk a rendszerből!", "danger")
            return redirect(url_for("home"))
    else:
        return render_template("security.html", form=form, title = "Ellenőrzés")

def security(password):
    if bcrypt.check_password_hash(current_user.password, password):
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



@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    form = TransferForm()
    if form.validate_on_submit():
        cleared_card_number = form.card_number.data.replace("-", "")
        cleared_to_card_number = form.to_card_number.data.replace("-", "")
        user = scan_user(cleared_to_card_number)[0]
        print(user)
        if int(cleared_card_number) == int(current_user.card_number) and int(form.cvc_code.data) == int(current_user.cvc_code):
            if user:
                if int(form.money.data) > int(current_user.balance):
                    flash("Nincs ennyi pénz a számládon!", "danger")
                    return redirect(url_for("transfer"))
                else:
                    current_user.balance -= form.money.data
                    user.balance += form.money.data
                    db.session.commit()
                    SuccesTransaction(current_user.username, current_user.email, user.username, user.card_number, form.money.data).send_email()
                    flash("Sikeres tranzakció, a részleteket továbbitottuk az e-mail címére!", "succes")
                    return redirect(url_for("home"))
            else:
                flash("Nem létezik a megadott kártyaszám!", "danger")
                return redirect(url_for("transfer"))
        else:
            flash("Rossz kártyaszám vagy CVC kód!", "danger")
            return redirect(url_for("transfer"))
    return render_template("transfer.html", title="Utalás", form=form)


def scan_user(card_number):
    user = User.query.filter_by(card_number=card_number).all()

    return user

    

@app.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html", title="Privacy")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sikeres kijelentkezés!", "succes")
    return redirect(url_for("home"))