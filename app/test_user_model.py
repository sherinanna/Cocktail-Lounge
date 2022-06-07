"""User model tests."""
#run test using following command
#   FLASK_ENV=production  python -m unittest test_user_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Review,Favorite

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests.
os.environ['DATABASE_URL'] = "postgresql:///cocktail-test"

# Now we can import app
from app import app

#enable testing mode and deactivate debug toolbar while testing
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# create the tables
db.create_all()

class UserModelTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u= User.signup("test1", "password", "myname","mylastname",30)
        uid = 1111
        u.id = uid

    
        db.session.commit()

        self.u = User.query.get(uid)
        self.uid = uid
        self.client = app.test_client()

    def tearDown(self):
        # here we are calling the tearDown inbuit function belonging to testcase. since 
        #  we are overwriting a function with  same name, we just want to make sure that we do all 
        # standard procedures in the base class. this is more of a convention
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            username="testuser",
            password="TEST_PASSWORD",
            first_name="john",
            last_name="thomas",
            age=25
         
        )

        db.session.add(u)
        db.session.commit()

        # User should have no reviews and favorites
        self.assertEqual(len(u.reviews), 0)
        self.assertEqual(len(u.favorites), 0)


#### Signup tests  ###
    def test_valid_signup(self):
        u_test = User.signup("testuser", "password","john","thomas", 25)
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testuser")
        self.assertEqual(u_test.first_name, "john")
        self.assertEqual(u_test.last_name, "thomas")
        self.assertEqual(u_test.age, 25)
        self.assertNotEqual(u_test.password, "password")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.signup(None, "password","john","thomas", 25)
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()


    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testuser", "","john","thomas", 25)
        
        with self.assertRaises(ValueError) as context:
            User.signup("testuser", None,"john","thomas", 25)
            
    def test_invalid_age_signup(self):
        invalid = User.signup("testuser", "password","john","thomas", None)
        uid = 123456789
        invalid.id = uid
        
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit() 
            
    
    # #### Authentication tests  ###
    def test_valid_authentication(self):
        u = User.authenticate(self.u.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u.username, "badpassword"))

    # test favorite a drink ###
    def test_favorite_drink(self):
        fav = Favorite(
            user_id=self.uid,
            cocktail_id=11007
        )
        self.u.favorites.append(fav)
    
        db.session.commit()

        favs= Favorite.query.filter(Favorite.user_id == self.uid).all()
        self.assertEqual(len(favs), 1)
        self.assertEqual(favs[0].cocktail_id, 11007)

    