from flask import render_template, redirect, url_for, flash, request
from ShoppingApp import app, db
from ShoppingApp.forms import RegisterForm, LoginForm
from ShoppingApp.models import User, Item, CartItem
from flask_login import login_user, logout_user, current_user

@app.route('/')
@app.route('/home')
def home():
    title = 'Home'
    return render_template('home.html', title=title)


@app.route('/product', methods=['GET'])
def product():
    title = 'Products'
    items = Item.query.all()
    print(items)
    return render_template('product.html', items=items, title=title)

@app.route('/product/add', methods=['POST'])
def productadd():
    itemname = request.args.get('itemname')
    itemprice = request.args.get('price')
    print("Account t shirt!")
    if itemname and itemprice:
        new_item = Item(itemname=itemname, itemprice=itemprice)
        db.session.add(new_item)  # add new item to db
        db.session.commit()  # commits all changes
        print("Shirt shirt")

@app.route('/cart', methods=['GET'])
def cart():
    title = 'Cart'
    cartitems = CartItem.query.all()
    cartadd()
    return render_template('cart.html', cartitems=cartitems, title=title)

@app.route('/cart/add', methods=['POST'])
def cartadd():
    itemname = request.args.get('itemname')
    itemquantity = request.args.get('itemquantity')
    itemprice = request.args.get('price')
    print("item in cart")
    if itemname and itemquantity and itemprice:
        new_item = CartItem(itemname=itemname, itemquantity=itemquantity, itemprice=itemprice)
        db.session.add(new_item)  # add new item to db
        db.session.commit()  # commits all changes
        print("inside cart if")

@app.route('/wishlist')
def wishlist():
    title = 'wishlist'
    return render_template('wishlist.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Login'
    form = LoginForm()

    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        print(current_user.is_authenticated)
        return redirect(url_for('product'))
    if form.validate_on_submit():
        user = User.query.filter_by(userName=form.userName.data).first()
        if user is None or not user.check_password(form.password.data):
            print("Wrong Password")
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('product'))

    return render_template('login.html', title=title, form=form)

@app.route('/logout')
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'Register'
    form = RegisterForm()
    if form.validate_on_submit():
        users = User(userName=form.userName.data, firstName=form.firstName.data,
                     lastName=form.lastName.data, email=form.email.data, CreditCard=form.CreditCard.data,
                     ccv=form.ccv.data)
        users.set_password(form.password.data)
        users.set_hint(form.hint.data)
        db.session.add(users)
        db.session.commit()
        print("Account Created!")


    return render_template('register.html', title=title, form=form)
