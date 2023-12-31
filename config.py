from fusionflare import app

SECRET_KEY = "KEY"
SQLALCHEMY_DATABASE_URI = "sqlite:///database.sql"



app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "example@gmail.com"
app.config["MAIL_PASSWORD"] = "password"
