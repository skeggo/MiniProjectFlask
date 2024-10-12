from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from flask_login import login_user,LoginManager





login_manager = LoginManager()




db = SQLAlchemy()




def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
    app.config['SECRET_KEY'] = 'c06286df2884b159e704102a'
    app.config['DEBUG'] = True
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt = Bcrypt(app)
    from routes import register_routes
    register_routes(app, db)

    migrate = Migrate(app, db)

    return app

flask_app = create_app()

with flask_app.app_context():
    from models import Item, User


    db.create_all()



if __name__ == '__main__':
    flask_app.run(host='0.0.0.0',debug=True)
