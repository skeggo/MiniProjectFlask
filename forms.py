from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import Item, User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already taken')
    def validate_email(self, email_to_check):
        email_address = User.query.filter_by(email=email_to_check.data).first()
        if email_address:
            raise ValidationError('Email address already taken')

    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20, message='Username must be between 3 and 20 characters.')
    ])

    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Please enter a valid email address.')
    ])

    password1 = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=5, message='Password must be at least 5 characters long.')
    ])

    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password1', message='Passwords must match.')
    ])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField(label='email', validators=[DataRequired()])
    password = PasswordField(label='password', validators=[DataRequired()])
    submit = SubmitField(label='Login')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell')