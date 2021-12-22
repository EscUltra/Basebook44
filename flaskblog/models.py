from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import login_manager
from flask import current_app
from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    #Each one create a Column that stors data for each user
    id = db.Column(db.Integer, primary_key=True)  #Creates column for and id that is an integer that is unique
    username = db.Column(db.String(20), unique=True, nullable=False) #Creates column for the useranme that is a string with a max_len of 20 char
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file =  db.Column(db.String(20), nullable=False, default="default.jpg") #the default is the dedault.jpg
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref='author', lazy=True) #A User can create many posts but a post cant have more than 1 user, gives Post access to the data in User

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)  #Make a token with a secret key from app.py and an experation time of 1800s
        return s.dumps({'user_id': self.id}).decode('utf-8')  #Acutally creates the token, with a payload of current user id

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id= s.loads(token)['user_id'] #tries to load token if the token = the users id
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f'User("{self.username}", "{self.email}", "{self.image_file}")'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #Gets the Id of the user who created the post

    def __repr__(self):
        return f'Post("{self.title}", "{self.date_posted}")'