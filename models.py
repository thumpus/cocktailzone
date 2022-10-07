from curses import use_env
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

class Favorite(db.Model):
    """favorite cocktails"""
    __tablename__= 'favorites'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    cocktail_id = db.Column(db.Integer)

class User(db.Model):
    """user model"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    favorites = db.relationship("Favorite", backref='user', primaryjoin ="User.id == Favorite.user_id")

    @classmethod
    def register(cls, username, email, password):
        """signs up the user and hashes password"""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """find user with mathcing username and pwd. if it finds the user, it returns that user object, if it can't it returns False"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False        


def connect_db(app):
    """connect to db"""
    db.app = app
    db.init_app(app)