from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class RegisterForm(FlaskForm):

     userName = StringField('User Name')
     firstName = StringField('User Name')
     lastName = StringField('User Name')
     email = StringField('Email')
     CreditCard = IntegerField('Credit Card Number')
     ccv = IntegerField('CCV Value')
     submit = SubmitField('Submit')



