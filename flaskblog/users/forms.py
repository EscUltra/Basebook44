
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) #creates a field in the form that requires data min 2 char max of 20

    email = StringField("Email",  validators=[DataRequired(), Email()])

    password = PasswordField("Password",  validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",  validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField("Sign up")

    def validate_username(self, username): #Validation checks to see if there already is a username in the database with that same username
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('That username is taken please choose another one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('That email is already in use.')



class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password",  validators=[DataRequired()])
    remember = BooleanField("Remember Me")


    submit = SubmitField("Login")






class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField("Email",  validators=[DataRequired(), Email()])

    picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField("Update")

    def validate_username(self, username): #Validation checks to see if the form username = the currnet users username if it doesent check to make sure that they cant change it to a email already in use 
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()

            if user:
                raise ValidationError('That username is taken please choose another one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()

            if user:
                raise ValidationError('That email is already in use.')




class RequestResetForm(FlaskForm):

    email = StringField("Email",  validators=[DataRequired(), Email()])

    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError('There is no account with that email you must register first')




class ResetPasswordForm(FlaskForm):

    password = PasswordField("Password",  validators=[DataRequired()])

    confirm_password = PasswordField("Confirm Password",  validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField('Reset Password')