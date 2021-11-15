from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = 'CoffeeLovers.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'the one key to rule them all'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Shops, locationsTable

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #tells flask how to load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #looks for primary key

    return app


def create_database(app):
    if not path.exists('website' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


#function to calculate the rating for coffee shops
def calculate_rating(rating):
    stars = [1,2,3,4,5]
    return round(sum(list(map(lambda a,b: a*b, stars, rating_list))) / sum(rating_list), 2)
