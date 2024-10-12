from time import sleep

import bcrypt

from market import db,login_manager

from flask_login import UserMixin


@login_manager.user_loader

def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer, nullable=False,default =400)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


    def check_password(self,attempted_password):
        return bcrypt.checkpw(attempted_password.encode('utf-8'), self.password_hash)


    def can_purchase(self,obj):
        return self.budget >= obj.price


    def __repr__(self):
        return '<User {}>'.format(self.username)


    def can_sell(self,obj):
        return obj in self.items
class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), unique=True, nullable=False)
    barcode = db.Column(db.String(70), unique=True, nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __init__(self,name, barcode, price):
        self.name = name
        self.barcode = barcode
        self.price = price
    def __repr__(self):
        return f'Item {self.name}'

    def buy(self,user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self,user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

