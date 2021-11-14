from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')


# index page
@views.route('/index')
def index():
    count = len(User.query.all())
    people = User.query.all()
    return render_template("index.html", users=count, lstOfUsers=people)


# list all of current users
@views.route('/users')
def get_users():
    people = User.query.all()

    # output = []
    # for person in people:
    # people_data = {'name': person.name, 'city': person.city, 'locations': person.locations}
    # output.append(people_data)

    return render_template("usersPage.html", lstOfUsers=people)
    # {"Users": output}


# search for a specific ID
@views.route('/users/<id>')
def get_user(id):
    person = User.query.get_or_404(id)

    # return {"name": person.name, "city": person.city, "locations": person.locations}
    return render_template("userInquiry.html", result=person)





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


######### begin location section #########

# view the shop location index
@views.route('/shops')
def shop_index():
    count = len(Location.query.all())
    shops = Location.query.all()
    return render_template("shopIndex.html", shops=count, lstOfShops=shops)


#add new shops via JSON
@views.route('/shops', methods=['POST'])
def add_shop():
    shop = Location(name=request.json['name'], rating=request.json['rating'], loc_id=request.json['loc_id'])
    db.session.add(shop)
    db.session.commit()
    return {'id': shop.id}


#add new shops via a form
@views.route("/form_shops")
def shop_form():
    return render_template("shopAddForm.html")


# receives data from the form and adds to DB
@views.route("/data_shops", methods=["POST", "GET"])
def shop_data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to sign up"
    if request.method == 'POST':
        shop = Location(name=request.form['name'], rating=request.form['rating'])
        form_data = request.form
        db.session.add(shop)
        db.session.commit()
        return render_template("shopData.html", form_data=form_data)


# delete a shop id
@views.route('/shops/<id>', methods=['DELETE'])
def del_shop(id):
    shop = Location.query.get(id)
    if shop is None:
        return {"Error": "404 Not Found"}
    db.session.delete(shop)
    db.session.commit()
    #return {"Message": "Account Deleted"}
    return render_template("shopDeletePage.html", shop=shop)