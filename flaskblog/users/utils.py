import secrets
import os
from PIL import Image
from flask import  url_for , current_app
from flaskblog import mail
from flaskblog.models import User 
from flask_mail import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path , 'static/images', picture_fn)
    out_size = (125 , 125)
    img = Image.open(form_picture)
    img.thumbnail(out_size)
    img.save(picture_path)
    return picture_fn

# reset password 

def send_reset_email(user):
    token = User.get_reset_token(user.id)
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email.
'''
    mail.send(msg)