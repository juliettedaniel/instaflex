from datetime import datetime
from extensions import db
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()




# Notes for me: db.relationship() signals SQLAlchemy to establish a relationship in the ORM, 
# and db.backref() creates a reverse relationship from Post to User,
# effectively linking the models in both directions

likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    liked_posts = db.relationship(
        'Post',
        secondary=likes,
        backref=db.backref('likers', lazy='dynamic')
    )

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash
    
    # Intentionally not putting 'password_hash' for security reasons
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

# By adding the likers relationship to the Post class in line 52, you establish the reverse 
# relationship from Post to User, indicating that a post can have multiple users who have liked it. This will allow you to retrieve the users who have liked a particular post.

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    image = db.Column(db.Text, nullable=False)
    caption = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    likers = db.relationship(
        'User',
        secondary=likes,
        backref=db.backref('liked_posts', lazy='dynamic')
    )

    def __init__(self, date, image, caption, user_id: int):
        self.date = date
        self.image = image
        self.caption = caption
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'image': self.image,
            'caption': self.caption,
            'user_id': self.user_id
        }

class Friendship(db.Model):
    __tablename__ = 'friendship'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id1 = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_id2 = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, user_id1: int, user_id2: int):
        self.user_id1 = user_id1
        self.user_id2 = user_id2

    def serialize(self):
        return {
            'id': self.id,
            'user_id1': self.user_id1,
            'user_id2': self.user_id2,
            'status': self.status,
            'created_at': self.created_at
        }
    
class Like(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __init__(self, user_id: int, post_id: int):
        self.user_id = user_id
        self.post_id = post_id

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id
        }