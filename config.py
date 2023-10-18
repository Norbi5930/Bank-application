from fusionflare import app

SECRET_KEY = "5eba80e13335ecb1442d3d3155ac6d5c"
SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"



app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "bnorbert0925@gmail.com"
app.config["MAIL_PASSWORD"] = "qalq xsmh qcud lkml"