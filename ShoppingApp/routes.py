from flask import render_template
from ShoppingApp import app, db
from ShoppingApp.forms import RegisterForm, LoginForm
from ShoppingApp.models import User, Items
from flask_login import login_user, logout_user

@app.route('/')
@app.route('/home')
def home():
    title = 'Home'
    return render_template('home.html', title=title)


@app.route('/product')
def high():
    title = 'products'
    return render_template('product.html', title=title)


@app.route('/cart')
def mid():
    title = 'cart'
    return render_template('cart.html', title=title)    


@app.route('/wishlist')
def low():
    title = 'wishlist'
    return render_template('wishlist.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Login'
    form = LoginForm()
    #if form.validate_on_submit():



    return render_template('login.html', title=title, form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'Register'
    form = RegisterForm()
    if form.validate_on_submit():
        users = User(userName=form.userName.data, firstName=form.firstName.data,
                     lastName=form.lastName.data, email=form.email.data, CreditCard=form.CreditCard.data,
                     ccv=form.ccv.data)
        users.set_password(form.password.data)
        users.set_secret_key(form.secret_key.data)
        db.session.add(users)
        db.session.commit()
        print("Account Created!")


    return render_template('register.html', title=title, form=form)
