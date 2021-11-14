from flask import Blueprint, render_template, request, flash, redirect , url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Shops, locationsTable

views = Blueprint('views', __name__)


@views.route('/')
def main():
    users = len(User.query.all())
    return render_template('main.html', user=current_user, users=users)


@views.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)


# index page
@views.route('/index')
def index():
    count = len(User.query.all())
    people = User.query.all()
    return render_template("index.html", users=count, lstOfUsers=people, user=current_user)


# list all of current users
@views.route('/users')
def get_users():
    people = User.query.all()

    # output = []
    # for person in people:
    # people_data = {'name': person.name, 'city': person.city, 'locations': person.locations}
    # output.append(people_data)

    return render_template("usersPage.html", lstOfUsers=people, user=current_user)
    # {"Users": output}


# search for a specific ID
@views.route('/users/<id>')
def get_user(id):
    person = User.query.get_or_404(id)

    # return {"name": person.name, "city": person.city, "locations": person.locations}
    return render_template("userInquiry.html", result=person, user=current_user)


# add a user via JSON input
@views.route('/users', methods=['POST'])
def add_user():
    user = User(name=request.json['name'], city=request.json['city'], locations=request.json['locations'],
                username=request.json['username'])
    db.session.add(user)
    db.session.commit()
    return {'id': user.id}


# delete a user id
@views.route('/users/<id>', methods=['DELETE'])
def del_user(id):
    user = User.query.get(id)
    if user is None:
        return {"Error": "404 Not Found"}
    db.session.delete(user)
    db.session.commit()
    return {"Message": "Account Deleted"}


######### begin shops section #########

# view the shop location index
@views.route('/shops')
def shop_index():
    count = len(Shops.query.all())
    shops = Shops.query.all()
    return render_template("shopIndex.html", shops=count, lstOfShops=shops, user=current_user)


#add new shops via JSON
@views.route('/shops', methods=['POST'])
def add_shop():
    shop = Shops(name=request.json['name'], rating=request.json['rating'], loc_id=request.json['loc_id'])
    db.session.add(shop)
    db.session.commit()
    return {'id': shop.id}


#add new shops via a form
@views.route("/form_shops", methods=['GET', 'POST'])
def shop_form():
    if request.method == 'POST':
        return render_template(url_for('views.shop_added'))
    return render_template("shopAddForm.html", user=current_user)


@views.route('/shop_added', methods=['GET', 'POST'])
def shop_added():
    form_data = request.form
    name = request.form.get('name')
    rating = request.form.get('rating')

    new_shop = Shops(name=name, rating=rating)

    db.session.add(new_shop)
    db.session.commit()
    return render_template('shopAdded.html', form_data=form_data, user=current_user)

# receives data from the form and adds to DB
"""""@views.route("/data_shops", methods=["POST", "GET"])
def shop_data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to sign up"
    if request.method == 'POST':
        name = request.form.get('name')
        rating = request.form.get('rating')

        new_shop = Shops(name=name, rating=rating)
        form_data = request.form
        db.session.add(new_shop)
        db.session.commit()
        return render_template("shopData.html", form_data=form_data, user=current_user)"""


# delete a shop id
@views.route('/shops/<id>', methods=['DELETE'])
def del_shop(id):
    shop = Shops.query.get(id)
    if shop is None:
        return {"Error": "404 Not Found"}
    db.session.delete(shop)
    db.session.commit()
    #return {"Message": "Account Deleted"}
    return render_template("shopDeletePage.html", shop=shop, user=current_user)
