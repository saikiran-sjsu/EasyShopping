from flask import render_template, redirect, url_for, flash, request
from ShoppingApp import app, db
from ShoppingApp.forms import RegisterForm, LoginForm, ForgotForm
from ShoppingApp.models import User, Item, CartItem, WishListItem, InvoiceItem
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
                                   itemquantity=int(request.form['quantity']),
                                   image=request.args.get('itemimage'),
                                   itemsize=request.form['itemsize'])
            quantityToAdd = int(request.form['quantity'])
            cat = request.args.get('category')
            print(cat)
            cartHasItem = db.session.query(CartItem).first() #Check to see if cart is empty
            if cartHasItem:
                itemFound = db.session.query(CartItem).filter_by(itemname=newCartItem.itemname).first()
                if itemFound:  # item exists in table already, update quantity
                    sizeFound = db.session.query(CartItem).filter_by(itemsize=newCartItem.itemsize).first()
                    print(sizeFound)
                    if sizeFound:
                        foundItemName = db.session.query(CartItem).filter_by(itemname=newCartItem.itemname).first().itemname
                        itemSizeFound = db.session.query(CartItem).filter_by(itemsize=newCartItem.itemsize).first().itemsize
                        foundItemQuant = db.session.query(CartItem).filter_by(itemname=newCartItem.itemname).first().itemquantity
                        foundItemQuant += quantityToAdd
                        print("Item already exists need quantity update")
                        db.session.query(CartItem).filter(CartItem.itemname == foundItemName).filter(CartItem.itemsize == itemSizeFound).update(
                            {'itemquantity': foundItemQuant})  #item exists in table already, update quantity
                        db.session.commit()
                        return redirect(url_for('cart'))
                    """else:
                        db.session.add(newCartItem)
                        db.session.commit()
                        return redirect(url_for('cart'))

                else: #item doesn't exist in cart yet
                    db.session.add(newCartItem)  # add new item to db
                    db.session.commit()  # commits all changes
                    return redirect(url_for('cart'))"""

            #else: #cart empty, add item
            db.session.add(newCartItem)  # add new item to db
            db.session.commit()  # commits all changes
            return redirect(url_for('cart'))

        elif request.form.get('addtowishlist'):
            newWSItem = WishListItem(itemname=request.args.get('itemname'),
                                     itemprice=request.args.get('itemprice'),
                                     image=request.args.get('itemimage'),
                                     itemsize=request.form['itemsize'])
            foundItemInWS = db.session.query(WishListItem).filter_by(itemname=newWSItem.itemname).first()
            if foundItemInWS:
                foundSizeInWS = db.session.query(WishListItem).filter_by(itemsize=newWSItem.itemsize).first()
                if not foundSizeInWS:
                    db.session.add(newWSItem)
                    db.session.commit()

            else:
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

        elif request.form.get('sortbycategories'):
             bycategories = db.session.query(Item).order_by(Item.category).order_by(Item.itemname).all()
             return render_template('product.html', items=bycategories, title=title)

    return render_template('product.html', items=items, title=title)

@app.route('/cart', methods=['GET','POST'])
def cart():
    title = 'Cart'
    cartitems = CartItem.query.all()
    totalsubprice = 0.00
    for item in cartitems:
        totalsubprice += (item.itemprice*item.itemquantity)
    tax = totalsubprice*(0.08)
    totalprice = tax + totalsubprice

    if request.method == 'POST':
        if request.form.get('removefromcart'):
            print("removing from cart")
            itemToRemove = request.args.get('itemname')
            print(itemToRemove)
            cartitemsize = request.args.get('itemsize')
            print(cartitemsize)
            db.session.query(CartItem).filter(CartItem.itemname == itemToRemove).filter(
                CartItem.itemsize == cartitemsize).delete()
            db.session.commit()
            return redirect(url_for('cart'))

        if request.form.get('updatequantity'):
            cartitemname = request.args.get('itemname')
            cartitemsize = request.args.get('itemsize')
            newquantity = int(request.form['quantity'])
            db.session.query(CartItem).filter(CartItem.itemname == cartitemname).filter(
                CartItem.itemsize == cartitemsize).update({'itemquantity':newquantity})
            db.session.commit()
            return redirect(url_for('cart'))

        if request.form.get('submitorder'):
            firstItem = cartitems.pop(0)
            itemsStr = firstItem.itemname + " " + \
                       firstItem.itemsize + " x" + \
                       str(firstItem.itemquantity) + " $" +\
                       str(firstItem.itemprice) + "0"
            db.session.query(CartItem).filter(CartItem.itemname == firstItem.itemname).filter(
                CartItem.itemsize == firstItem.itemsize).delete()

            for item in cartitems:
                itemsStr += "#" + item.itemname + " " +\
                            item.itemsize + " x" +\
                            str(item.itemquantity) + " $" +\
                            str(item.itemprice) + "0"
                db.session.query(CartItem).filter(CartItem.itemname == item.itemname).filter(
                    CartItem.itemsize == item.itemsize).delete()
            #print(itemsStr)
            newInvoiceItem = InvoiceItem(items=itemsStr,
                                         subtotal=totalsubprice,
                                         total=totalprice,
                                         tax=tax)
            db.session.add(newInvoiceItem)
            db.session.commit()
            return redirect(url_for('invoice'))

    return render_template('cart.html', cartitems=cartitems, title=title, subtotal=totalsubprice, tax=tax, totalprice=totalprice)

@app.route('/invoice', methods=['GET'])
def invoice():
    title = 'Invoice(s)'
    items = InvoiceItem.query.all()
    return render_template('invoice.html', invoicelist=items, title=title)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():

    title = 'Forgot Password'

    form = ForgotForm()
    print('hiss')
    user = User.query.filter_by(userName=form.userName.data).first()
    if form.validate_on_submit():
        # user = User.query.filter_by(userName=form.userName.data).first()
        print(user)
        print('foo')
        print(form.question.data)
        print(user.check_secret_key)
        print(user.check_secret_key(form.question.data))
        if user.check_secret_key(form.question.data):
            print('moo')
            return redirect(url_for('reset'))
        print('forgot not working')
    return render_template('forgot.html', title=title, form=form)

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    title = 'Reset Password | Task Organizer'
    form = ForgotForm()
    print('hi')
    if form.validate_on_submit():
        print('hello')
        user = User.query.filter_by(userName=form.userName.data).first()
        user.set_password(form.reset_password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset.html', title=title, form=form)



@app.route('/wishlist', methods=['GET','POST'])
def wishlist():
    title = 'wishlist'
    wishlistitems = WishListItem.query.all()

    if request.method == 'POST':
        if request.form.get('addtocart'):
            print("It's a POST request on wishlist page")
            newCartItemFromWL = CartItem(itemname=request.args.get('itemname'),
                                         itemprice=request.args.get('itemprice'),
                                         itemquantity=int(request.form['quantity']),
                                         image=request.args.get('itemimage'),
                                         itemsize=request.args.get('itemsize'))
            quantityToAdd = int(request.form['quantity'])
            listHasAnyItems = db.session.query(CartItem).first()  # Check to see if cart is empty
            if listHasAnyItems:
                itemFound = db.session.query(CartItem).filter_by(itemname=newCartItemFromWL.itemname).first()
                if itemFound:# item exists in table already, update quantity
                    sizeFound = db.session.query(CartItem).filter_by(itemsize=newCartItemFromWL.itemsize).first()
                    print(sizeFound)
                    if sizeFound:
                        foundItemName = db.session.query(CartItem).filter_by(itemname=newCartItemFromWL.itemname).first().itemname
                        itemSizeFound = db.session.query(CartItem).filter_by(
                            itemsize=newCartItemFromWL.itemsize).first().itemsize
                        foundItemQuant = db.session.query(CartItem).filter_by(
                            itemname=newCartItemFromWL.itemname).first().itemquantity
                        foundItemQuant += quantityToAdd
                        db.session.query(CartItem).filter(CartItem.itemname == foundItemName).filter(
                            CartItem.itemsize == itemSizeFound).update({'itemquantity': foundItemQuant})
                        db.session.commit()
                        return redirect(url_for('cart'))
                    """else:
                        db.session.add(newCartItemFromWL)
                        db.session.commit()
                        return redirect(url_for('cart'))

                else:  # item doesn't exist in cart yet
                    db.session.add(newCartItemFromWL)  # add new item to db
                    db.session.commit()  # commits all changes
                    return redirect(url_for('cart'))"""

            #else:  # cart empty, add item
            db.session.add(newCartItemFromWL)  # add new item to db
            db.session.commit()  # commits all changes
            return redirect(url_for('cart'))

        elif request.form.get('removefromwishlist'):
            itemToRemoveName = request.args.get('itemname')
            itemToRemoveSize = request.args.get('itemsize')
            db.session.query(WishListItem).filter(WishListItem.itemname == itemToRemoveName).filter(
                WishListItem.itemsize == itemToRemoveSize).delete()
            db.session.commit()
            return redirect(url_for('wishlist'))


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
