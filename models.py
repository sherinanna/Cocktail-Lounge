
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db=SQLAlchemy()

def connect_db(app):
    """Connect the database to the Flask app"""
    
    db.app=app
    db.init_app(app)
    
# 1. User model
class User(db.Model):
    """ User model """
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username=db.Column(db.Text,unique=True,nullable=False)
    password=db.Column(db.Text, nullable=False)
    first_name=db.Column(db.Text, nullable=False)
    last_name=db.Column(db.Text, nullable=False)
    age=db.Column(db.Integer,nullable=False)
    
    # define 1:m relation from user to reviews
    reviews=db.relationship('Review',backref='user')

# define relation from user to favorites. Actualy user can favorite many drinks and same drink can eb
# favorited by many users. so do i need to define this as m:m .(but dont have drinks table)
    favorites=db.relationship('Favorite')
    
    @classmethod
    def signup(cls, username, password, first_name, last_name, age):
        """Register a user, hashing their password and add the user to the database"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            age=age
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


    
# 2.  Reviews model
class Review(db.Model):
    """user reviews on cocktails"""
    __tablename__='reviews'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    review=db.Column(db.Text, nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    cocktail_id=db.Column(db.Integer, nullable=False)
    

# 3.  Favorites model
class Favorite(db.Model):
    """Saved drinks for a user"""
    
    __tablename__='favorites'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id', ondelete='cascade'))
    cocktail_id=db.Column(db.Integer, nullable=False)
    

    