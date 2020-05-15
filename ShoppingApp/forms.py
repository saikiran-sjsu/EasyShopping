from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField


# Forms for registering users on the registration page
class RegisterForm(FlaskForm):

     userName = StringField('User Name')
     firstName = StringField('User Name')
     lastName = StringField('User Name')
     email = StringField('Email')
     CreditCard = IntegerField('Credit Card Number')
     ccv = IntegerField('CCV Value')
     password = PasswordField('Password')
     hint = PasswordField('Secret Key')
     submit = SubmitField('Submit')


# Forms for users to log in on the log in page
class LoginForm(FlaskForm):
     userName = StringField('User Name')
     password = PasswordField('Password')
     submit = SubmitField('Submit')


# Forms for users when they forget their password
class ForgotForm(FlaskForm):
     userName = StringField('User Name')
     question = PasswordField('Secret Question')
     reset_password = PasswordField('Password')
     reset = SubmitField('Reset')


