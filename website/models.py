from . import db
from flask_login import UserMixin

#db.Model.metadata.reflect(db.engine)

# helper table
locationsTable = db.Table('locations',
                          db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                          db.Column('shop_id', db.Integer, db.ForeignKey('shops.id'), primary_key=True))


# create table for coffee shops
class Shops(db.Model):
    __tablename__ = 'shops'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Text)
    rating = db.Column(db.Float)
    count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"{self.name} - {self.rating}"


# create table for the users
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    name = db.Column(db.String(80))
    locations = db.relationship('Shops', secondary=locationsTable, lazy='subquery',
                                backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"{self.name} - {self.email} - {self.locations}"


