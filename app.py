from flask import Flask, render_template, redirect, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from sqlalchemy.exc import IntegrityError
import requests

from models import connect_db, db, User, Trip
from forms import UserForm, LoginForm, DeleteForm #TripForm


API_BASE_URL = 'http://api.bart.gov/api'
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///bart"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)


# /, /register, /login, /logout, /users/<username>, /users/<username>/delete


# 1- Home page will be redirected to /register.
@app.route('/')         
def home_page():
    return redirect('/register')


# 2- When the user successfully registers or logs in, store the username in the session.
@app.route('/register', methods=['GET', 'POST'])
def register_user():

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
    
        user = User.register(username, password, email)

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('users/register.html', form=form)
        session['username'] = user.username

        return redirect(f"/users/{user.username}")
    
    else:
        return render_template('users/register.html', form=form)


# 3- When the user successfully registers or logs in, store the username in the session.
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username/password.']
            return render_template('users/login.html', form=form)
    
    return render_template('users/login.html', form=form)


# 4- log out
@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("See you later!", "info")
    return redirect('/login')


# 5- Delete user
@app.route('/users/<username>/delete', methods=["POST"])
def delete_user(username):
    """
    Remove the user from the database and also delete all their trips. 
    Clear any user information in the session and redirect to /. 
    Make sure that only the user who is logged in can successfully delete their account
    """
    if 'username' not in session or username != session['username']:
        flash("Please login first!", "danger")
        raise Unauthorized()

        
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")
    return redirect('/login')


# 6- Show information about the given user & all of the trips that the user has saved.
@app.route('/users/<username>')
def show_user(username):
    """
    For each saved trip, display a button to usave the trip.
    Have a link that sends you to a page to search new trips and a button to delete the user Make sure that only the user who is logged in can successfully view this page.
    """
    #When the user successfully registers or logs in, store the username in the session.
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    form = DeleteForm()

    trips = Trip.query.all()

    return render_template("users/index.html", user=user, form=form, trips=trips)        





### New Trip ###

# /users/<username>/new, /users/<username>/saved, /trip-plan,

"""Return all routes from the API"""
@app.route('/users/<username>/new', methods=['GET', 'POST'])
def new_trip(username):
    if "username" not in session or username != session['username']:
        flash("Please login first!", "danger")
        return redirect('/')

    #form = FeedbackForm()



    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=session['username'])
        
        db.session.add(feedback)
        db.session.commit()

        flash('Feedback Created!', 'success')
        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedbacks/new.html", form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def update_feedback(feedback_id):
    """
    GET /feedback/<feedback-id>/update
    Display a form to edit feedback
    Make sure that only the user who has written that feedback can see this form **

    POST /feedback/<feedback-id>/update
    Update a specific piece of feedback and redirect to /users/<username> 
    Make sure that only the user who has written that feedback can update it
    """
    feedback = Feedback.query.get(feedback_id)

    if 'username' not in session or feedback.username != session['username']:
        flash("Please login first!", "danger")
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback
    POST /feedback/<feedback-id>/delete
    Delete a specific piece of feedback and redirect to /users/<username>
    Make sure that only the user who has written that feedback can delete it
    """
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or feedback.username != session['username']:
        flash("Please login first!", "danger")
        return redirect('/login')

    form = DeleteForm()
    
    if feedback.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        flash("Feedback deleted!", "info")
    
    return redirect(f"/users/{feedback.username}")
