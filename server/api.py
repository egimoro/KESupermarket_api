import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy  
from flask_migrate import Migrate 


api = Flask(__name__)
api.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('user')

db = SQLAlchemy(api)
migrate = Migrate(api, db)

class KEsupModel(db.Model):
    __tablename__ = 'Kenyan Supermarkets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    no_of_items = db.Column(db.Integer())
    total = db.Column(db.Float())
    paid = db.Column(db.Float())
    change = db.Column(db.Float())
    type_ = db.Column(db.String())
    food = db.Column(db.Boolean())
    drinks = db.Column(db.Boolean())

    def __init__(self, name, no_of_items, total,
                 paid, change, type_, food, drinks):
        
        self.name = name
        self.no_of_items = no_of_items
        self.total = total 
        self.paid = paid
        self.change = change
        self.type_ = type_
        self.food = food
        self.drinks = drinks
        


    def __repr__(self):
        return f"<KEsup {self.name}>"
    
db.create_all()
  
@api.route('/')
def hello():
    return {"hello": "world"}

@api.route('/kesupermarkets', methods=['POST','GET'])
def handle_supermarkets():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_supermarket = KEsupModel(name=data['name'], no_of_items=data['no_of_items'],
                                        paid=data['paid'], food=data['food'], 
                                        change=data['change'], type_=data['type_'],
                                        drinks=data['drinks'], total=data['total'])

            db.session.add(new_supermarket)
            db.session.commit()
            return {"message": f"supermarket {new_supermarket.name} has been created successfully."}
        else:
            return {"error": "the request payload is not in JSON format"}
    
    elif request.method == 'GET':
        
        kesup = KEsupModel.query.all()
        results = [
        {
        "name": supmkt.name,
        "no_of_items": supmkt.no_of_items,
        "total": supmkt.total,
        "paid": supmkt.paid,
        "type": supmkt.food,
        "drinks": supmkt.drinks,
        "food": supmkt.food,
        "change": supmkt.change
        } for supmkt in kesup
    ]

    return {"count": len(results), "Supermarkets": results}

@api.route('/kesupermarkets/<int:kesup_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_supermarket(kesup_id):
    kesup = KEsupModel.query.get_or_404(kesup_id)

    if request.method == 'GET':
        response = {
            "name": kesup.name,
            "no_of_items": kesup.no_of_items,
            "total": kesup.total,
            "paid": kesup.paid,
            "type_": kesup.type_,
            "drinks": kesup.drinks,
            "food": kesup.food
        }
        return {"message": "success", "Supermarket": response} 
    
    elif request.method == 'PUT':
        data = request.get_json()
        kesup.name = data['name']
        kesup.no_of_items = data['no_of_items']
        kesup.total = data['total']
        kesup.paid = data['paid']
        kesup.type_ = data['type_']
        kesup.drinks = data['drinks']
        kesup.food = data['food']
        db.session.add(kesup)
        db.session.commit()
        return {"message": f"supermarket {kesup.name} successfully updated"} 

    elif request.method == 'DELETE':
        db.session.delete(kesup)
        db.session.commit()
        return {"message": f"supermarket {kesup.name} successfully deleted"}



if __name__ == '__main__':
    api.run(debug=True)