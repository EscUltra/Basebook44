import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) # f_name is the file without .jpg,  f_ext is just .jpg
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) #creates path to profile_pics

    output_size = (125, 125)
    i = Image.open(form_picture)  #Resize images
    i.thumbnail(output_size)
    i.save(picture_path) #saves picture to profile_pics

    return picture_fn #returns the file name of new profile



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='escbean90@gmail.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then ignore this email and no changes will be made
    '''
    mail.send(msg)