from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField


class RegisterForm(FlaskForm):

     userName = StringField('User Name')
     firstName = StringField('User Name')
     lastName = StringField('User Name')
     password = PasswordField('Password')
     email = StringField('Email')
     CreditCard = IntegerField('Credit Card Number')
     ccv = IntegerField('CCV Value')
     submit = SubmitField('Submit')


class LoginForm(FlaskForm):
     username = StringField('User Name')
     password = PasswordField('Password')
     submit = SubmitField('Submit')



