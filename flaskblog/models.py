from datetime import datetime
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Follow(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    profile_image = db.Column(db.String(20) , nullable=True , default="default.jpg")

    followers = db.relationship(
        'Follow',
        foreign_keys=[Follow.followed_id],
        backref='followed',
        lazy='dynamic'
    )

    following = db.relationship(
        'Follow',
        foreign_keys=[Follow.follower_id],
        backref='follower',
        lazy='dynamic'
    )

    def is_following(self, user):
        return Follow.query.filter_by(
            follower_id=self.id,
            followed_id=user.id
        ).first() is not None



    def get_reset_token(user_id, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': user_id})

    def verify_reset_token(token, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=expires_sec)['user_id']
        except:
            return None
        return user_id

    
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Views Likes

    views = db.Column(db.Integer , default=0)
    Likes = db.relationship('Like' , backref='post' , lazy=True , cascade="all, delete-orphan")

class Like(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Comment(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    content = db.Column(db.Text , nullable=False)
    date_posted = db.Column(db.DateTime , default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


    user = db.relationship('User', backref='comments', lazy=True)
    post = db.relationship('Post', backref='comments', lazy=True)


class Notification(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    message = db.Column(db.String(255) , nullable=False)
    link = db.Column(db.String(255) , nullable=False)
    is_read = db.Column(db.Boolean , default=False)
    created_at = db.Column(db.DateTime , default=datetime.utcnow)



