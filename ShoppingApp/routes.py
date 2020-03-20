from flask import app
from flask import render_template
from ShoppingApp import app


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