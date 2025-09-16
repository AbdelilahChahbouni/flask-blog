from flask_wtf import FlaskForm
from wtforms import StringField , BooleanField ,  PasswordField , SubmitField , ValidationError 
from wtforms.validators import DataRequired , Email , Length , EqualTo
from flask_wtf.file import FileAllowed , FileField
from flaskblog.models import User 
from flask_login import current_user





class RegistrationForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired() , Length(min=2 , max=20)])
    email = StringField('Email' , validators=[DataRequired() , Email()])
    password = PasswordField('Password' , validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password' , validators=[DataRequired() , EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self , username):
            user = User.query.filter_by(username=username.data).first()
            if user:
                 raise ValidationError("that username is token plaease take anaother one")
    def validate_email(self , email):
            user = User.query.filter_by(email=email.data).first()
            if user:
                 raise ValidationError("that eamil is token plaease take anaother one")


class LoginForm(FlaskForm):
    email = StringField('Email' , validators=[DataRequired() , Email()])
    password = PasswordField('Password' , validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username' , validators=[DataRequired() , Length(min=2 , max=20)])
    email = StringField('Email' , validators=[DataRequired() , Email()])
    picture = FileField("Update Profile Picture " , validators=[FileAllowed(['png','jpg'])])
    submit = SubmitField('Update')

    def validate_username(self , username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                 raise ValidationError("that username is token plaease take anaother one")
    def validate_email(self , email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                 raise ValidationError("that email is token plaese take anathor one")
            

class RequestResetForm(FlaskForm):
     email = StringField('Email' , validators=[DataRequired() , Email()])
     submit = SubmitField('Reset Password')
     def validate_email(self , email):
            user = User.query.filter_by(email=email.data).first()
            if user is None:
                 raise ValidationError("There is no Account with that email , You musst register first")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password' , validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password' , validators=[DataRequired() , EqualTo('password')])
    submit = SubmitField('Reset Password')
