from flask import render_template, redirect, url_for, flash, request
from ShoppingApp import app, db
from ShoppingApp.forms import RegisterForm, LoginForm
from ShoppingApp.models import User, Item, CartItem, WishListItem
from flask_login import login_user, logout_user, current_user

@app.route('/')
@app.route('/home')
def home():
    title = 'Home'
    return render_template('home.html', title=title)

@app.route('/product', methods=['GET','POST'])
def product():
    title = 'Products'
    items = Item.query.all()
    print(items)

    if request.method == 'POST':
        print(request.form.get('addtocart'))
        if request.form.get('addtocart'):
            print("Its a POST request on product page")
            newCartItem = CartItem(itemname=request.args.get('itemname'),
                                   itemprice=request.args.get('itemprice'),
                                   itemquantity=int(request.form['quantity']))
            quantityToAdd = int(request.form['quantity'])
            print(quantityToAdd)
            cartHasItem = db.session.query(CartItem).first() #Check to see if cart is empty
            if cartHasItem:
                itemFound = db.session.query(CartItem).filter_by(itemname=newCartItem.itemname).first()
                if itemFound:
                    foundItemName = db.session.query(CartItem).filter_by(itemname=newCartItem.itemname).first().itemname
                    foundItemQuant = db.session.query(CartItem).filter_by(itemname=newCartItem.itemname).first().itemquantity
                    foundItemQuant += quantityToAdd
                    print("Item already exists need quantity update")
                    db.session.query(CartItem).filter(CartItem.itemname == foundItemName).update( #item exists in table already, update quantity
                        {'itemquantity': foundItemQuant})
                    db.session.commit()
                    return redirect(url_for('cart'))

                else: #item doesn't exist in cart yet
                    db.session.add(newCartItem)  # add new item to db
                    db.session.commit()  # commits all changes
                    return redirect(url_for('cart'))

            else: #cart empty, add item
                db.session.add(newCartItem)  # add new item to db
                db.session.commit()  # commits all changes
                return redirect(url_for('cart'))

        elif request.form.get('addtowishlist'):
            newWSItem = WishListItem(itemname=request.args.get('itemname'),
                                   itemprice=request.args.get('itemprice'))

            foundItemWS = db.session.query(WishListItem).filter_by(itemname=newWSItem.itemname).first()

            if not foundItemWS:
                db.session.add(newWSItem)
                db.session.commit()

        elif request.form.get('sorthighlow'):
            itemshighlow = db.session.query(Item).order_by(Item.itemprice.desc())
            return render_template('product.html', items=itemshighlow, title=title)

        elif request.form.get('sortlowhigh'):
            itemslowhigh = db.session.query(Item).order_by(Item.itemprice)
            return render_template('product.html', items=itemslowhigh, title=title)

        elif request.form.get('sortbyname'):
            itemsbyname = db.session.query(Item).order_by(Item.itemname)
            return render_template('product.html', items=itemsbyname, title=title)

    return render_template('product.html', items=items, title=title)

@app.route('/cart', methods=['GET','POST'])
def cart():
    title = 'Cart'
    cartitems = CartItem.query.all()
    totalprice = 0.00
    for item in cartitems:
        totalprice += (item.itemprice*item.itemquantity)

    if request.method == 'POST':
        if request.form.get('removefromcart'):
            print("trying to delete")
            itemToRemove = request.args.get('itemname')
            """db.session.query(CartItem).filter(itemname=itemToRemove).delete()"""
            db.session.query(CartItem).filter(CartItem.itemname == itemToRemove).delete()
            db.session.commit()
            return redirect(url_for('cart'))
            

    return render_template('cart.html', cartitems=cartitems, title=title, totalprice=totalprice)

@app.route('/wishlist', methods=['GET','POST'])
def wishlist():
    title = 'wishlist'
    wishlistitems = WishListItem.query.all()
    print(wishlistitems)

    if request.method == 'POST':
        print("It's a POST request on wishlist page")
        newCartItemFromWL = CartItem(itemname=request.args.get('itemname'),
                                     itemprice=request.args.get('itemprice'),
                                     itemquantity=int(request.form['quantity']))
        quantityToAdd = int(request.form['quantity'])
        print("quantity from wish list")
        print(quantityToAdd)
        cartHasItem = db.session.query(CartItem).first()  # Check to see if cart is empty
        if cartHasItem:
            itemFound = db.session.query(CartItem).filter_by(itemname=newCartItemFromWL.itemname).first()
            if itemFound:
                foundItemName = db.session.query(CartItem).filter_by(itemname=newCartItemFromWL.itemname).first().itemname
                foundItemQuant = db.session.query(CartItem).filter_by(
                    itemname=newCartItemFromWL.itemname).first().itemquantity
                foundItemQuant += quantityToAdd
                print("Item already exists need quantity update")
                db.session.query(CartItem).filter(CartItem.itemname == foundItemName).update(
                    # item exists in table already, update quantity
                    {'itemquantity': foundItemQuant})
                db.session.commit()
                return cart()

            else:  # item doesn't exist in cart yet
                db.session.add(newCartItemFromWL)  # add new item to db
                db.session.commit()  # commits all changes
                return cart()

        else:  # cart empty, add item
            db.session.add(newCartItemFromWL)  # add new item to db
            db.session.commit()  # commits all changes
            return cart()

    return render_template('wishlist.html', items=wishlistitems, title=title)


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
