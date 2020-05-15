from flask import render_template, redirect, url_for, flash, request
from ShoppingApp import app, db
from ShoppingApp.forms import RegisterForm, LoginForm, ForgotForm
from ShoppingApp.models import User, Item, CartItem, WishListItem, InvoiceItem
from flask_login import login_user, logout_user, current_user

#Home page
@app.route('/')
@app.route('/home')
def home():
    title = 'Home'
    return render_template('home.html', title=title)


#Decorator & functions related to the cart page
@app.route('/cart', methods=['GET','POST'])
def cart():
    title = 'Cart'
    #Get the list of items from the cart table
    cartitems = CartItem.query.all()
    #Find the subtotal, tax and total based on the items in the cart table
    totalsubprice = 0.00
    for item in cartitems:
        totalsubprice += (item.itemprice*item.itemquantity)
    tax = totalsubprice*(0.08)
    totalprice = tax + totalsubprice

    if request.method == 'POST':
        # Gets the name & size of an item to search for a row with the same
        #   values to delete that row from the cart table
        if request.form.get('removefromcart'):
            itemToRemove = request.args.get('itemname')
            cartitemsize = request.args.get('itemsize')
            db.session.query(CartItem).filter(CartItem.itemname == itemToRemove).filter(
                CartItem.itemsize == cartitemsize).delete()
            db.session.commit()
            return redirect(url_for('cart'))

        # Gets the name and size of an item to search for a row with the same values
        #   to update that row's quantity attribute
        #   to update that row's quantity attribute
        if request.form.get('updatequantity'):
            cartitemname = request.args.get('itemname')
            cartitemsize = request.args.get('itemsize')
            newquantity = int(request.form['quantity'])
            db.session.query(CartItem).filter(CartItem.itemname == cartitemname).filter(
                CartItem.itemsize == cartitemsize).update({'itemquantity':newquantity})
            db.session.commit()
            return redirect(url_for('cart'))

        # Create string that is a list of all the items in the cart table, then create
        #   an invoice containing the list of items, subtotal, tax and total before adding
        #   invoice to the table of invoices
        if request.form.get('submitorder'):
            firstItem = cartitems.pop(0)
            itemsStr = firstItem.itemname + " " + \
                       firstItem.itemsize + " x" + \
                       str(firstItem.itemquantity) + " $" +\
                       str(firstItem.itemprice) + "0"
            db.session.query(CartItem).filter(CartItem.itemname == firstItem.itemname).filter(
                CartItem.itemsize == firstItem.itemsize).delete()
            # Concatenate the information of all the items that are still in the cart
            for item in cartitems:
                itemsStr += "#" + item.itemname + " " +\
                            item.itemsize + " x" +\
                            str(item.itemquantity) + " $" +\
                            str(item.itemprice) + "0"
                db.session.query(CartItem).filter(CartItem.itemname == item.itemname).filter(
                    CartItem.itemsize == item.itemsize).delete()

            newInvoiceItem = InvoiceItem(items=itemsStr,
                                         subtotal=totalsubprice,
                                         total=totalprice,
                                         tax=tax)
            db.session.add(newInvoiceItem)
            db.session.commit()
            return redirect(url_for('invoice'))

    return render_template('cart.html', cartitems=cartitems, title=title, subtotal=totalsubprice, tax=tax, totalprice=totalprice)


#decorator and functions for the invoice
@app.route('/invoice', methods=['GET'])
def invoice():
    title = 'Invoice(s)'
    # Originally, the invoice page contained all invoices currently in the database
    items = InvoiceItem.query.all()
    # Then a list with only the latest invoice was created so that the invoice page
    #   only displayed the most recent invoice
    lastitemarray =[]
    lastitem = db.session.query(InvoiceItem).order_by(InvoiceItem.id.desc()).first()
    lastitemarray.append(lastitem)

    return render_template('invoice.html', invoicelist=lastitemarray, title=title)

@app.route('/admin')
def admin():
    title = 'admin'
    # tasks = Task.query.filter_by(user_id=current_user.id)

    users = User.query.all()

    return render_template('admin.html', title=title, users=users)


#decorator and exection of the forgot password feature
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    title = 'Forgot Password'
    form = ForgotForm()
    user = User.query.filter_by(userName=form.userName.data).first()

    if form.validate_on_submit():
        # print statements for testing the forgot password feature
        # user = User.query.filter_by(userName=form.userName.data).first()
        # print(form.question.data)
        # print(user.check_secret_key)
        # print(user.check_secret_key(form.question.data))
        if user.check_secret_key(form.question.data):
            print('moo')
            return redirect(url_for('reset'))
        print('forgot not working')
    return render_template('forgot.html', title=title, form=form)


#decorator & functions on the product page
@app.route('/product', methods=['GET','POST'])
def product():
    title = 'Products'
    items = Item.query.all()

    if request.method == 'POST':
        # Create a cart item, then check if that item in a specific size already exists in the cart,
        #   if it does, then just update the quantity.
        #   If the cart is empty, then just add the new item to the cart.
        if request.form.get('addtocart'):
            changesize = request.form['itemsize']
            newCartItem = CartItem(itemname=request.args.get('itemname'),
                                   itemprice=request.args.get('itemprice'),
                                   itemquantity=int(request.form['quantity']),
                                   image=request.args.get('itemimage'),
                                   itemsize=changesize.capitalize())
            quantityToAdd = int(request.form['quantity'])
            # Check to see if cart is empty
            cartHasItem = db.session.query(CartItem).first()
            if cartHasItem:
                itemFound = db.session.query(CartItem).filter_by(itemname=newCartItem.itemname).first()
                if itemFound:
                    sizeFound = db.session.query(CartItem).filter_by(itemsize=newCartItem.itemsize).first()
                    if sizeFound:
                        foundItemName = db.session.query(CartItem).filter_by(itemname=newCartItem.itemname).first().itemname
                        itemSizeFound = db.session.query(CartItem).filter_by(itemsize=newCartItem.itemsize).first().itemsize
                        foundItemQuant = db.session.query(CartItem).filter_by(itemname=newCartItem.itemname).first().itemquantity
                        foundItemQuant += quantityToAdd
                        db.session.query(CartItem).filter(CartItem.itemname == foundItemName).filter(CartItem.itemsize == itemSizeFound).update(
                            {'itemquantity': foundItemQuant})  # update quantity
                        db.session.commit()
                        return redirect(url_for('cart'))

            db.session.add(newCartItem)
            db.session.commit()
            return redirect(url_for('cart'))

        # Create a wishlist item using data from the html page, then find if the item is already in the wish lis
        #   If the item is already there, do nothing, otherwise, add the item to the wish list
        elif request.form.get('addtowishlist'):
            changesize = request.form['itemsize']
            newWSItem = WishListItem(itemname=request.args.get('itemname'),
                                     itemprice=request.args.get('itemprice'),
                                     image=request.args.get('itemimage'),
                                     itemsize=changesize.capitalize())
            foundItemInWS = db.session.query(WishListItem).filter_by(itemname=newWSItem.itemname).first()
            if foundItemInWS:
                foundSizeInWS = db.session.query(WishListItem).filter_by(itemsize=newWSItem.itemsize).first()
                if not foundSizeInWS:
                    db.session.add(newWSItem)
                    db.session.commit()
            else:
                db.session.add(newWSItem)
                db.session.commit()

        # The following 4 groups of code retrieves the user's choice from the html page
        #   and a query is done to sort the list of items in the database that are shown on
        #   the products page.
        sort_choice = request.form.get('dropdown')
        # Sort by price: high to low
        if sort_choice == "highlow":
            itemshighlow = db.session.query(Item).order_by(Item.itemprice.desc())
            return render_template('product.html', items=itemshighlow, title=title)
        # Sort by price: low to high
        elif sort_choice == "lowhigh":
            itemslowhigh = db.session.query(Item).order_by(Item.itemprice)
            return render_template('product.html', items=itemslowhigh, title=title)
        # Sort by the item's name in alphabetical order
        elif sort_choice == "alphabet":
            itemsbyname = db.session.query(Item).order_by(Item.itemname)
            return render_template('product.html', items=itemsbyname, title=title)
        # Sort based on an item's category and within each category, sort alphabetically
        elif sort_choice =="bycategory":
            bycategories = db.session.query(Item).order_by(Item.category).order_by(Item.itemname).all()
            return render_template('product.html', items=bycategories, title=title)

    return render_template('product.html', items=items, title=title)

# Decorator and function for resetting the password
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

# Decorator and functions related to the wish list page
@app.route('/wishlist', methods=['GET','POST'])
def wishlist():
    title = 'Wishlist'
    wishlistitems = WishListItem.query.all()

    if request.method == 'POST':
        # When the 'add to cart button is pressed, create a cart item using data from the html,
        #   then find if the item already exists in the cart, if it does then add the item
        #   to the cart, otherwise, update the quantity of that item
        if request.form.get('addtocart'):
            changesize = request.form['itemsize']
            newCartItemFromWL = CartItem(itemname=request.args.get('itemname'),
                                         itemprice=request.args.get('itemprice'),
                                         itemquantity=int(request.form['quantity']),
                                         image=request.args.get('itemimage'),
                                         itemsize=changesize.capitalize())
            quantityToAdd = int(request.form['quantity'])
            # Check to see if cart is empty
            listHasAnyItems = db.session.query(CartItem).first()
            if listHasAnyItems:
                itemFound = db.session.query(CartItem).filter_by(itemname=newCartItemFromWL.itemname).first()
                # item exists in table already, update quantity
                if itemFound:
                    sizeFound = db.session.query(CartItem).filter_by(itemsize=newCartItemFromWL.itemsize).first()
                    if sizeFound:
                        foundItemName = db.session.query(CartItem).filter_by(
                            itemname=newCartItemFromWL.itemname).first().itemname
                        itemSizeFound = db.session.query(CartItem).filter_by(
                            itemsize=newCartItemFromWL.itemsize).first().itemsize
                        foundItemQuant = db.session.query(CartItem).filter_by(
                            itemname=newCartItemFromWL.itemname).first().itemquantity
                        foundItemQuant += quantityToAdd
                        db.session.query(CartItem).filter(CartItem.itemname == foundItemName).filter(
                            CartItem.itemsize == itemSizeFound).update({'itemquantity': foundItemQuant})
                        db.session.commit()
                        return redirect(url_for('cart'))

            # cart empty, add item
            db.session.add(newCartItemFromWL)
            db.session.commit()
            return redirect(url_for('cart'))

        # If the user presses the 'remove' button for an item, search for that item in the database
        #   and once found, remove it from the wish list table
        elif request.form.get('removefromwishlist'):
            itemToRemoveName = request.args.get('itemname')
            itemToRemoveSize = request.args.get('itemsize')
            db.session.query(WishListItem).filter(WishListItem.itemname == itemToRemoveName).filter(
                WishListItem.itemsize == itemToRemoveSize).delete()
            db.session.commit()
            return redirect(url_for('wishlist'))

    return render_template('wishlist.html', items=wishlistitems, title=title)

# Decorator and function to validate a user when they are trying to log in
@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Login'
    form = LoginForm()

    # For a user to access buttons to add and move items to and from the wish
    #   list and cart, the user must first log in, otherwise, they can only
    #   view the product list
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

# Decorator and function for when users press the logout button
@app.route('/logout')
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))

# Decorator and function for users to input their information and create a user
#   account, which will create a row containing information on a user into the
#   user table in the database
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
        return redirect(url_for('login'))
    return render_template('register.html', title=title, form=form)
