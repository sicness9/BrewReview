from flask import Blueprint, render_template, request, flash, redirect, url_for, session
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
    shops = Shops.query.filter(Shops.user_id == (current_user.get_id()))
    return render_template('home.html', user=current_user, shops=shops)


# index page
@views.route('/index')
def index():
    count = len(User.query.all())
    people = User.query.all()
    return render_template("index.html", users=count, lstOfUsers=people, user=current_user)


# list all of current users
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


# delete a user id
@views.route('/users/<id>', methods=['DELETE'])
def del_user(id):
    user = User.query.get(id)
    if user is None:
        return {"Error": "404 Not Found"}
    db.session.delete(user)
    db.session.commit()
    return {"Message": "Account Deleted"}


######### begin coffee shops section #########

# view the shop location index
@views.route('/shops')
def shop_index():
    count = len(Shops.query.all())
    shops = Shops.query.all()

    #this section is a work in progress, trying to grab all the shops with duplicate names and average their ratings
    #to display on the shop index page. Trying to figure out how to enter raw SQL using SQLAlchemy, it's not cooperating :)
    """
    for line in shops:
        name = db.session.fetchone()[1]

        db.session.execute("SELECT count from Shops WHERE name = ?", (name,))
        row = db.session.fetchone()
        if row is None:
            db.session.execute('INSERT INTO Shops (name, count) VALUES (?,1)', (name,))
        else:
            db.session.execute('UPDATE Shops SET  count = count + 1 WHERE name = ?', (name,))
        db.session.commit()

    sqlstr = 'SELECT name, count FROM Shops ORDER BY count'

    for row in db.execute(sqlstr):
        row = str(row[0], row[1])
        print(row)"""
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


#idea for adding/rating
#ask for name of the shops then query DB to see if it exists
#if exists prompt for a rating and then add the rating to rating column
#maybe set rating column to be a list of ratings and then get the average rating
@views.route('/shop_added', methods=['GET', 'POST'])
@login_required
def shop_added():
    form_data = request.form
    name = request.form.get('name')
    rating = request.form.get('rating')
    user_id = current_user.get_id()

    new_shop = Shops(name=name, rating=rating, user_id=user_id)

    db.session.add(new_shop)
    db.session.commit()
    return render_template('shopAdded.html', form_data=form_data, user=current_user)


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
