from flask_login import UserMixin

from ShoppingApp import db
from werkzeug.security import generate_password_hash,check_password_hash
from ShoppingApp import login

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(64), unique=True, nullable=False)
    firstName = db.Column(db.String(128))
    lastName = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    CreditCard = db.Column(db.String(128), unique=True)
    ccv = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128), nullable=False)
    hint = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User:{}>'.format(self.userName)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_hint(self, hint):
        self.hint = generate_password_hash(hint)

    def check_secret_key(self, hint):
        return check_password_hash(self.hint, hint)

class Item(db.Model):
    """Data model for items."""

    __tablename__ = 'table_of_items'
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(64), unique=True, nullable=False)
    itemprice = db.Column(db.Float)

class CartItem(db.Model):

    __tablename__ = 'cart_table'
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(64), unique=True, nullable=False)
    itemquantity = db.Column(db.Integer)
    itemprice = db.Column(db.Float)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

if __name__ == '__main__':
    db.create_all()



