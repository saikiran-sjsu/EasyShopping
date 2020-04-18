from ShoppingApp import db
from werkzeug.security import generate_password_hash,check_password_hash


class User(db.Model):

    __UserTable__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(64), unique=True, nullable=False)
    firstName = db.Column(db.String(128))
    lastName = db.Column(db.String(128))
    password = db.Column(db.String(128), nullable=False)
    secret_key = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), index=True, unique=True)
    CreditCard = db.Column(db.String(128), unique=True)
    ccv = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '<User:{}>'.format(self.userName)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        self.password = check_password_hash(self.password, password)

    def set_secret_key(self, secret_key):
        self.password = generate_password_hash(secret_key)

    def check_secret_key(self, secret_key):
        self.password = check_password_hash(self.secret_key, secret_key)



class Items(db.Model):
    __UserTable__ = 'Items'
    id = db.Column(db.Integer, primary_key=True)

if __name__ == '__main__':
    db.create_all()




