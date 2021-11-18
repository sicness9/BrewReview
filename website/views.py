import flask_login
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from sqlalchemy.sql import func

from . import db
from .models import User, Shops, locationsTable
from sqlalchemy.sql import func

views = Blueprint('views', __name__)

#Cover page
@views.route('/')
def main():
    users = len(User.query.all())
    return render_template('main.html', user=current_user, users=users)


@views.route('/home')
@login_required
def home():
    # query for the shops the signed in user has added/rated
    shops = Shops.query.filter(Shops.user_id == (current_user.get_id()))
    return render_template('home.html', user=current_user, shops=shops)


#user index page
@views.route('/user_index')
def index():
    count = len(User.query.all())
    people = User.query.all()
    return render_template("index.html", users=count, lstOfUsers=people, user=current_user)


#about us page
@views.route('/aboutus')
def about_us():
    return render_template("aboutus.html", user=current_user)



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


#delete request
@views.route('/account/delete-request', methods=['GET', 'POST'])
def del_account_request():
    if request.method == 'POST':
        return render_template(url_for('views.del_user'))
    return render_template("userDeleteRequest.html", user=current_user)


# delete account
@views.route('/account/account_delete', methods=['POST', 'DELETE'])
def del_user():
    email = request.form.get('email')
    if email is None:
        return {"Error": "404 Not Found"}
    #query DB to look for the entered email from the form and and assign to user object
    user = User.query.filter(User.email == request.form.get('email')).first()
    flask_login.logout_user() #log out the user before deletion
    db.session.delete(user)
    db.session.commit()
    if request.method == 'DELETE':
        return render_template(url_for('views.acc_deleted_view'))
    return render_template('accountDeleted.html', user=current_user)



######### begin coffee shops section #########

# view the shop location index
@views.route('/shops', methods=['GET', 'POST'])
def shop_index():
    count = len(Shops.query.all()) #grab the number of shops in the db
    if request.method == 'GET':
        return render_template("shopIndex.html", shops=count, user=current_user)
    if request.method == 'POST':
        name = request.form.get('name')
        return render_template(url_for('views.shop_rating', name=name), user=current_user)


#user can search for a coffee shop and view the total average ratings
@views.route('/shops/<name>/ratings', methods=['GET', 'POST'])
def shop_rating(name):
    name = request.form.get('name')
    #SQL query will search for all entries of the entered shop name and grab all the ratings values and average them out
    averageCheck = db.session.query(func.avg(Shops.rating).label('Average Rating')).filter(Shops.name == name)
    averageRating = find_average(averageCheck)
    return render_template('shopQuery.html', user=current_user, averageRating=averageRating, name=name)


#function to clean up the results of the SQL query
def find_average(averageCheck):
    for i in averageCheck:
        numReplace = str(i).replace('(', ',')
        numSplit = numReplace.strip(',')
        avg = numSplit[:3]
        return avg


#add new shops via JSON
@views.route('/shops/JSON', methods=['POST'])
def add_shop():
    shop = Shops(name=request.json['name'], rating=request.json['rating'], loc_id=request.json['loc_id'])
    db.session.add(shop)
    db.session.commit()
    return {'id': shop.id}


#add new shops via a form
@views.route("/form_shops", methods=['GET', 'POST'])
def shop_form():
    if request.method == 'POST':
        return render_template(url_for('views.shop_add'))
    return render_template("shopAddForm.html", user=current_user)


#function will take all entered information from shop_form() and add to DB
@views.route('/shop_add', methods=['GET', 'POST'])
@login_required
def shop_add():
    name = request.form.get('name')
    form_data = request.form
    rating = request.form.get('rating')
    user_id = current_user.get_id()
    new_shop = Shops(name=name, rating=rating, user_id=user_id)
    db.session.add(new_shop)
    db.session.commit()
    return render_template('shopAdded.html', form_data=form_data, user=current_user)


# delete a shop id // not available to end user in the app, do not want to delete too many shops
@views.route('/shops/<id>', methods=['DELETE'])
def del_shop(id):
    shop = Shops.query.get(id)
    if shop is None:
        return {"Error": "404 Not Found"}
    db.session.delete(shop)
    db.session.commit()
    #return {"Message": "Account Deleted"}
    return render_template("shopDeletePage.html", shop=shop, user=current_user)
