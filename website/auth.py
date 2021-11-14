from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


#login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@auth.route('/logout')
def logout():
    return "<p>Logout</p>"


@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(name) < 2:
            flash('Name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Password do not match', category='error')
        elif len(password1) < 7:
            flash('Password is too short', category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template('signup.html')


#After first step of gathering email and password // ask these questions on next screen before account is created
#@views.route("/signup2", methods=['POST'])
#def signup2():
#    user = User(name=request.form['name'], email=request.form['email'], password1=request.form['password1'],
#                password2=request.form['password2'])
#    form_data = request.form
#    return render_template("signup2.html", form_data=form_data, user=user)

# receives data from the form and adds to DB
#@views.route("/data/", methods=["POST", "GET"])
#def data():
#    if request.method == 'GET':
#        return f"The URL /data is accessed directly. Try going to '/form' to sign up"
#    if request.method == 'POST':
#        user = User(name=request.form['name'], email=request.form['email'], password1=request.form['password1'],
#                password2=request.form['password2'])
#        form_data = request.form
#        db.session.add(user)
#        db.session.commit()
#        return render_template("data.html", form_data=form_data)
