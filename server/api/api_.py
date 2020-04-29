import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy  
from flask_migrate import Migrate 
from flask_restful import Resource, Api, abort
from flask_marshmallow import Marshmallow

api_ = Flask(__name__)
api = Api(api_)
api_.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('user_')

db = SQLAlchemy(api_)
ma = Marshmallow(api_)
migrate = Migrate(api_, db)

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
    location = db.Column(db.String())

    def __init__(self, name, no_of_items, total,
                 paid, change, type_, food, drinks, location):
        
        self.name = name
        self.no_of_items = no_of_items
        self.total = total 
        self.paid = paid
        self.change = change
        self.type_ = type_
        self.food = food
        self.drinks = drinks
        self.location = location


    def __repr__(self):
        return f"<KEsup {self.name}>"


class KesupSchema(ma.Schema):
    class Meta:
        fields = ('name', 'no_of_items', 'total',
                 'paid', 'change', 'type_', 'food', 'drinks', 'location')


kesup_schema = KesupSchema()
kesup_schemas = KesupSchema(many=True)



class HelloRestWorld(Resource):
    def get(self):
        return {'hello': 'rest world'}


class KesupList(Resource):
    def get(self):
        all_supermarkets = KEsupModel.query.all()     
        results = kesup_schema.dump(all_supermarkets)
        for result in results:
            unitprice = result['total']/result['no_of_items']

        return {'Supermarkets': results, 'unitprice': round(unitprice, 2)}

    def post(self):
        name = request.json['name']
        no_of_items = request.json['no_of_items']
        total = request.json['total']
        paid = request.json['paid']
        change = request.json['change']
        type_ = request.json['type_'] 
        food = request.json['food']
        drinks = request.json['drinks']
        location = request.json['location']

        new_supermarket = KEsupModel(name, no_of_items, total, paid, change, type_, food, drinks,
                                    location)  

        

        db.session.add(new_supermarket)
        db.session.commit()
        result = kesup_schema.dump(new_supermarket) 
        unitprice = total/no_of_items

        return {'Supermarkets': result, 'Unit Price': unitprice} 

class KEsup(Resource):
    def get(self, kesup_id):
        kesup = KEsupModel.query.get(kesup_id)
        if kesup is not None:
            result = kesup_schema.dump(kesup)
            return result
        else:
            abort("Supermarket not found")  

    

api.add_resource(HelloRestWorld, '/')
api.add_resource(KesupList, '/api/kesupermarkets')
api.add_resource(KEsup, '/api/kesupermarkets/<int:kesup_id>')  
 
  
if __name__ == '__main__':
    api_.run(debug=True)  