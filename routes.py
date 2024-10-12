from wsgiref.util import request_uri

from flask import render_template, request, redirect, url_for, flash,request
from flask_login import login_user,logout_user
from werkzeug.security import generate_password_hash
from models import Item, User
from forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm
from market import db
from flask_login import login_required,current_user

def register_routes(app, db):
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/market',methods=['GET', 'POST'])
    @login_required
    def market():
        purchase_form = PurchaseItemForm()
        sell_form = SellItemForm()
        if request.method == "POST":
            purchased_item = request.form.get('purchased_item')
            p_item_object = Item.query.filter_by(name=purchased_item).first()
            if p_item_object:
                if current_user.can_purchase(p_item_object):
                    p_item_object.buy(current_user)
                    flash(f"You have successfully purchased {purchased_item}!", "success")
                else:
                    flash("You do not have enough funds to purchase this item.", "danger")
            sold_item = request.form.get('sell_item')
            s_item_object = Item.query.filter_by(name=sold_item).first()
            if s_item_object:
                if current_user.can_sell(s_item_object):
                    s_item_object.sell(current_user)
                    flash(f"You have successfully selled {sold_item}!", "success")
                else:
                    flash("You do not have enough funds to sell the item.", "danger")
            return redirect(url_for('market'))
        if request.method == 'GET':
            items = Item.query.filter_by(owner = None)
            owned_items = Item.query.filter_by(owner = current_user.id)
            return render_template('market.html', items=items,purchase_form = purchase_form,owned_items = owned_items,sell_form = sell_form)

    @app.route('/register', methods=['GET', 'POST'])
    def register_page():
        form = RegisterForm()
        if form.validate_on_submit():

            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash("Email already exists.", category='danger')
                return render_template('register.html', form=form)

            try:
                user_to_create = User(
                    username=form.username.data,
                    email=form.email.data,
                    password=form.password1.data
                )
                db.session.add(user_to_create)
                db.session.commit()

                print("User created successfully!")
                return redirect(url_for('home'))

            except Exception as e:
                db.session.rollback()
                flash(f"An error occurred while creating the user: {str(e)}", category='danger')
                print(f"Error: {e}")

        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login_page():
        form = LoginForm()
        if form.validate_on_submit():
            attempted_user = User.query.filter_by(email = form.email.data).first()
            if attempted_user and attempted_user.check_password(attempted_password = form.password.data):
                login_user(attempted_user)
                flash("Login successful!", category='success')
                return redirect(url_for('market'))
            else:
                flash("Login failed. Check your email and password.", category='danger')
        return render_template('login.html',form = form)



    @app.route('/logout')
    def logout_page():
        logout_user()
        flash("You have been logged out.", category='success')
        return redirect(url_for('home'))

