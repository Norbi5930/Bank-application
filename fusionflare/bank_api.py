from fusionflare.models import User
from flask_restful import Resource
from flask import request 
from fusionflare import db



class BankAPI(Resource):
    def get(self, card_number):
        user = User.query.filter_by(card_number=card_number).first()

        if user:
            return {"balance": user.balance}
        else:
            return {"error": "A megadott kártyaszám nem érvényes!"}, 404
        
    
    def post(self, card_number):
        user = User.query.filter_by(card_number=card_number).first()
        cvc_code = int(request.form.get("cvc_code"))
        if user and user.cvc_code == cvc_code:
            try:
                money = int(request.form.get("money"))
                if user.balance >= money:
                    user.balance -= money
                    db.session.commit()
                    return {"success": True, 'message': 'Sikeres feltöltés', 'new_balance': user.balance}
                else:
                    return {"success": False, "error": "Nincs elegendő pénz a számládon!"}
            except ValueError:
                return {"success": False, 'error': 'Érvénytelen összeg formátum'}
        else:
            return {"success": False, 'error': 'Felhasználó nem található'}, 404