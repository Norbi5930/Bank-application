from flask_mail import Mail, Message


from fusionflare import app 


mail = Mail(app)



class SuccessRegister:
    def __init__(self, username, card_number, send_mail):
        self.username = username
        self.card_number = card_number
        self.email = send_mail
    

    def send_email(self):
        number = 0
        card_number = ""
        for numbers in str(self.card_number):
            if number == 4:
                card_number += "-"
                number = 0
            number += 1
            card_number += numbers
        try:
            msg = Message("Sikeres regisztráció!", sender="FusionFlare@gmail.com", recipients=[self.email])
            msg.body = f"Üdv, {self.username}! \n Ön sikeresen regisztrált az oldalunkon! \n A kártyaszáma: {card_number}"
            mail.send(msg)
            return 
        except Exception as error:
            return error
        

class NewLogin:
    def __init__(self, username, send_email):
        self.username = username
        self.email = send_email
    
    def send_email(self):
        try:
            msg = Message("Új bejelentkező!", sender="FusionFlare@gmail.com", recipients=[self.email])
            msg.body = f"Kedves {self.username}! \n Egy új bejelentkezést észleltünk a fiókjában, ha nem ön volt az, ajánljuk, hogy változtassa meg a jelszavát! \n Ha viszont ön volt az akkor hagyja figyelmen kívül ezt az üzenetet!"
            mail.send(msg)
            return
        except Exception as error:
            return error
        


class PasswordChange:
    def __init__(self, username, email, link):
        self.username = username
        self.email = email
        self.link = link

    
    def send_email(self):
        try:
            msg = Message("Jelszó váltás", sender="FusionFlare@gmail.com", recipients=[self.email])
            msg.body = f"Kedves {self.username} \n Ezzel a linkel tudja megváltoztatni a jelszavát: {self.link}"
            mail.send(msg)
            return
        except Exception as error:
            return error
        
class SuccessTransaction:
    def __init__(self, username, email, to_username, to_card_number, money):
        self.username = username
        self.email = email
        self.to_username = to_username
        self.to_card_number = to_card_number
        self.money = money
    
    def send_email(self):
        try:
            msg = Message("Sikeres tranzakció!", sender="FusionFlare@gmail.com", recipients=[self.email])
            msg.body = f"Kedves {self.username}. \n Sikeres tranzakciót hajtott végre! \n Sikeres tranzakciót hajtott végre {self.to_username} személyel, a következő kártyaszámra: {self.to_card_number}! \n A pontos utalt összeg: {self.money}$"
            mail.send(msg)
        except Exception as error:
            return error
