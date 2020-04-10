from ShoppingApp import db


class User(db.Model):

    __UserTable__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(64), unique=True, nullable=False)
    firstName = db.Column(db.String(128))
    lastName = db.Column(db.String(128))
    email = db.Column(db.String(128), index=True, unique=True)
    CreditCard = db.Column(db.String(128), unique=True)
    ccv = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '<User:{}>'.format(self.userName)


class Items(db.Model):
    __UserTable__ = 'Items'
    id = db.Column(db.Integer, primary_key=True)

if __name__ == '__main__':
    db.create_all()




