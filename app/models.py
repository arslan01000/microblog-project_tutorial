from datetime import datetime, timezone
from hashlib import md5
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(64), index=True, unique=True)
    email = sa.Column(sa.String(120), index=True, unique=True)
    password_hash = sa.Column(sa.String(256))
    about_me = sa.Column(sa.String(140))
    last_seen = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship with the Post model
    posts = relationship("Post", back_populates="author", lazy='select')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class Post(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    body = sa.Column(sa.String(140))
    timestamp = sa.Column(sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), index=True)

    # Relationship with the User model
    author = relationship("User", back_populates="posts")

    def __repr__(self):
        return '<Post {}>'.format(self.body)
