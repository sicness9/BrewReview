from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


#login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #verify that the user exists in db
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password): #check if password entered equals password in db for this user
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) #(remember=True)unless server restarts or user clears cache/logout will stay signed in
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist', category='error')
    return render_template('login.html', user=current_user)


#send user to sign in page after sign out
@auth.route('/logout')
@login_required #cannot access this route unless user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


#sign up function
@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() #check if email already exists in DB
        if user:
            flash('This email already exists', category='error')
        elif len(email) < 4:
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
            login_user(new_user, remember=True, force=True)
            flash('Account created successfully!', category='success')
            return redirect(url_for('views.main'))

    return render_template('signup.html', user=current_user)


#WIP After first step of gathering email and password // ask these questions on next screen before account is created
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
