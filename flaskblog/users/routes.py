from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form  = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #Take in password in forms.py and turn it into a encripted string that will be put into the database
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #stores form data in variable
        db.session.add(user) #readys the database
        db.session.commit() #adds user to database
        flash('Your account has been created!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title="Register", form=form)



@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form  = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #check if the email the user put in the form is in the database
        if user and bcrypt.check_password_hash(user.password, form.password.data):  #if the user email exists in the database and the hashed password compated to the form password equals True
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') #When trying to access account without logging, it redirects to login page
            return redirect(next_page) if next_page else redirect(url_for('main.home')) #(up) if you login from there, it redirects you to the page you were trying to go to
        else:
            flash("Login unsuccessful check email and password.", "danger")
    return render_template('login.html', title="Login", form=form)




@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm() #Gets the data from the for
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data) #send the image data from the form into the save_picture function which encodes, saves, and returns the image
            current_user.image_file = picture_file #sets the new image as the picture
        current_user.username = form.username.data #Change the current users username and email
        current_user.email = form.email.data
        db.session.commit() #Update database
        flash("Your Account has been Updated", "success")
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username  #Put the information in the database into the form to change them
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) #stores the current users image file
    return render_template('account.html', title="Account", image_file=image_file, form=form) #renders account html that gives the html access to the image_file and the form UpdateAccountForm




@users.route("/user/<string:username>")  #Show all posts from a user
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404() #Get the first data of the user from the username that will be passed into the http
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)   #Get only the posts by the user passed in the http. Order post from newest to oldest. Number of posts per page
    return render_template("user_posts.html", posts=posts, user=user)




@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:   #If user is already logged in then dont give them access to this route
        return redirect(url_for('main.home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()   #Get the data of the user whos email was sent into the form
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Reset Password", form=form)




@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:   #If user is already logged in then dont give them access to this route
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)   #From the emial when they clikc the link the token will be passed to the http which will be sent to this func to see if its valid and if it is get the User data
    if user is None:   #If the token from the func in forms.py does not veryify the token
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #Take in new password password in and turn it into a encripted string that will be put into the database
        user.password = hashed_password
        db.session.commit() #adds user to database
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset Password", form=form)