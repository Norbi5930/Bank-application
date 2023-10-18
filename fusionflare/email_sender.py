from flask_mail import Mail, Message


from fusionflare import app 


mail = Mail(app)



class SuccesRegister:
    def __init__(self, username, card_number, send_mail):
        self.username = username
        self.card_number = card_number
        self.email = send_mail
    

    def send_email(self):
        try:
            msg = Message("Sikeres regisztráció!", sender="FusionFlare@gmail.com", recipients=[self.email])
            msg.body = f"Üdv, {self.username}! \n Ön sikeresen regisztrált az oldalunkon! \n A kártyaszáma: {self.card_number}"
            mail.send(msg)
            return True
        except Exception as error:
            return False
        
