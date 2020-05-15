from flask_login import UserMixin
from ShoppingApp import db
from werkzeug.security import generate_password_hash,check_password_hash
from ShoppingApp import login

# Models connects the application to the database so that data stored in the
#   app.db file can be accessed and displayed to the front end
# Each class represents a table in the database by showing the attributes &
#   data type of each column

# Contains the schema for the table of users in the database
# Also handles hashing of sensitive info so they can't be viewed in
#   the database
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

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_hint(self, password):
        self.hint = generate_password_hash(password)

    def check_secret_key(self, password):
        return check_password_hash(self.hint, password)

    def __repr__(self):
        return '<User:{}>'.format(self.userName)


# Contains the schema for the list of items that are sold in the website
#   that are displayed in the products page
class Item(db.Model):

    __tablename__ = 'table_of_items'
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(64), unique=True, nullable=False)
    itemprice = db.Column(db.Float)
    category = db.Column(db.String(64), nullable=False)
    image = db.Column(db.String(150), nullable=False)


# Contains the schema for the list of items that are currently in the cart
#   and have not yet been submitted as an order.  Will also keep track of the
#   quantity the user wants of each item
class CartItem(db.Model):

    __tablename__ = 'cart_table'
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(64), nullable=False)
    itemprice = db.Column(db.Float)
    image = db.Column(db.String(150), nullable=False)
    itemquantity = db.Column(db.Integer)
    itemsize = db.Column(db.String(64), nullable=False)


# Contains the schema for the list of items that are currently in
#   the wish list
class WishListItem(db.Model):

    __tablename__ = 'wishlist_table'
    id = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(64), nullable=False)
    itemprice = db.Column(db.Float)
    image = db.Column(db.String(150), nullable=False)
    itemsize = db.Column(db.String(64), nullable=False)


# Contains the schema for invoices being stored in the database
#   Items are stored as a long string that is processed in routes & parsed
#   only when it is displayed on the invoice html
class InvoiceItem(db.Model):

    __tablename__ = 'invoice_table'
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.String(10000), nullable=False)
    subtotal = db.Column(db.Float)
    total = db.Column(db.Float)
    tax = db.Column(db.Float)

# To load users for logging in
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


if __name__ == '__main__':
    db.create_all()



