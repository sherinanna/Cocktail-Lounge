"""Review model tests."""
#run test using following command
#  FLASK_ENV=production  python -m unittest test_review_model.py


import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Review,Favorite

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests
os.environ['DATABASE_URL'] = "postgresql:///cocktail-test"

# Now we can import app
from app import app

#enable testing mode and deactivate debug toolbar while testing
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# create the tables
db.create_all()

class ReviewModelTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 999
        u = User.signup("test1", "password", "myname","mylastname",30)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_review_model(self):
        """Does basic model work?"""
        
        r = Review(
            review="great drink",
            user_id=self.uid,
            cocktail_id=11007
        )

        db.session.add(r)
        db.session.commit()

        # User should have 1 review
        self.assertEqual(len(self.u.reviews), 1)
        self.assertEqual(self.u.reviews[0].review, "great drink")

    