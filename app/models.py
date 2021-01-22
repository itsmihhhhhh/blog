from app import db
from app import bcrypt
from datetime import datetime

tag = db.Table('tag', db.Model.metadata,
    db.Column('blogId', db.Integer, db.ForeignKey('blog.id')),
    db.Column('categoryId', db.Integer, db.ForeignKey('category.id'))
)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    blog = db.relationship('Blog', backref='user', lazy='dynamic')
    followed = db.relationship('User', secondary=followers,
    primaryjoin=(followers.c.follower_id == id),
    secondaryjoin=(followers.c.followed_id == id),
    backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return (self.id)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Blog.query.join(followers, (followers.c.followed_id == Blog.author)).filter(followers.c.follower_id == self.id)
        return followed.order_by(Blog.date.desc())

    def __repr__(self):
        return 'name - {}'.format(self.name)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    blog = db.relationship('Blog',secondary=tag)

    def __repr__(self):
        return 'category - {}'.format(self.name)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String(2000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.relationship('Category',secondary=tag)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'title {}'.format(self.title)
