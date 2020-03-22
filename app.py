from ShoppingApp import app
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://dbuser:password@localhost:5432/items_api"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class ItemsModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    price = db.Column(db.Float())

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Item {self.name}>"


#@app.route('/')
#def hello():
#	return {"hello": "world"}


@app.route('/items', methods=['POST', 'GET'])
def handle_items():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_item = ItemsModel(name=data['name'], price=data['price'])

            db.session.add(new_item)
            db.session.commit()

            return {"message": f"item {new_item.name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}

    elif request.method == 'GET':
        items = ItemsModel.query.all()
        results = [
            {
                "name": item.name,
                "price": item.price
            } for item in items]

        return {"count": len(results), "items": results, "message": "success"}


@app.route('/items/<item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_car(item_id):
    item = ItemsModel.query.get_or_404(item_id)

    if request.method == 'GET':
        response = {
            "name": item.name,
            "price": item.price
        }
        return {"message": "success", "item": response}

    elif request.method == 'PUT':
        data = request.get_json()
        item.name = data['name']
        item.price = data['price']

        db.session.add(item)
        db.session.commit()
        
        return {"message": f"item {item.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        
        return {"message": f"Car {item.name} successfully deleted."}


if __name__ == '__main__':
    app.run(debug=True)
