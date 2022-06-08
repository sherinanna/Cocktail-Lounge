"""Test the view functions in  the app"""

# run tests as
#    FLASK_ENV=production python -m unittest test_views.py

import os
from unittest import TestCase
from models import db, connect_db,User, Review,Favorite
from cocktails import Cocktail

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests
os.environ['DATABASE_URL'] = "postgresql:///cocktail-test"

# Now we can import app
from app import app, CURR_USER_KEY

#enable testing mode and deactivate debug toolbar while testing
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Don't have WTForms use CSRF at all, since it's a pain to test
app.config['WTF_CSRF_ENABLED'] = False


# create the tables
db.create_all()

class ViewTestCase(TestCase):
    """Test view ffunction"""

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()
        
        self.u = User.signup("test1", "password", "myname","mylastname",30)
        self.uid = 111
        self.u.id=self.uid
        
        db.session.commit()
        
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    def test_homepage(self):
        with self.client as c:
            resp = c.get("/")
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Mixed Bag", str(resp.data))
            self.assertIn("ADVANCED SEARCH", str(resp.data))

    def test_cocktail_favorite(self):
        """If logged in, can user favorite a drink"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid

            resp = c.post("/cocktails/11007/favorite", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            favorites =Favorite.query.filter(Favorite.cocktail_id==11007).all()
            self.assertEqual(len(favorites), 1)
            self.assertEqual(favorites[0].user_id, self.uid)

    def test_cocktail_unfavorite(self):
        """If logged in, can user unfavorite a drink"""
        # first favorite a drink
        drink_id=11007
        fav=Favorite(user_id=self.uid,cocktail_id=drink_id)
        db.session.add(fav)
        db.session.commit() 
        
        f = Favorite.query.filter(Favorite.user_id==self.uid and Favorite.cocktail_id==drink_id) .one()
        
        # Now we are sure that user likes the cocktail with id 11007
        self.assertIsNotNone(f)
        
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid

            resp = c.post(f"/cocktails/{drink_id}/favorite", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            favorites =Favorite.query.filter(Favorite.cocktail_id==drink_id).all()
            self.assertEqual(len(favorites), 0)
           
        
    def test_unauthenticated_unfavorite(self):
        """If not logged in can user unfavorite a drink"""
        # first favorite a drink
        drink_id=11007
        fav=Favorite(user_id=self.uid,cocktail_id=drink_id)
        db.session.add(fav)
        db.session.commit() 


        f = Favorite.query.filter(Favorite.user_id==self.uid and Favorite.cocktail_id==drink_id) .one()
        self.assertIsNotNone(f)
       
        fav_count = Favorite.query.count() 

        with self.client as c:
            resp = c.post(f"/cocktails/{drink_id}/favorite", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            self.assertIn("Please login to proceed", str(resp.data))

            # The number of favorites has not changed since making the request
            self.assertEqual(fav_count, Favorite.query.count() )
            
    def test_add_review(self):
        """Can logged in user add a review?"""
        drink_id=11007
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post(f"/cocktails/{drink_id}/reviews", data={"review": "besr drink ever"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            review = Review.query.one()
            self.assertEqual(review.review, "besr drink ever")
            
    def test_add_no_session(self):
        """ Can user add review without logging in"""
        with self.client as c:
            resp = c.post("/cocktails/11007/reviews", data={"review": "besr drink ever"}, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Please login to proceed", str(resp.data))
    
    
    def test_review_delete(self):
        """Can a logged in user delete his review """
        r = Review(
            id=1234,
            review="this is a great drink",
            user_id=self.uid,
            cocktail_id=11007
        )
        db.session.add(r)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid

            resp = c.post("/reviews/1234/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            r= Review.query.get(1234)
            self.assertIsNone(r)
 
 
    def test_unauthorized_review_delete(self):
        """Can a user delete another user's review """
        
        user=User.signup("unauthorized-user", "password", "testname","mylastname",33)
        user.id=678
        
        #review belongs to user with id 111
        r = Review(
            id=1234,
            review="this is a great drink",
            user_id=self.uid,
            cocktail_id=11007
        )
        db.session.add_all([user,r])
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 678

            resp = c.post("/reviews/1234/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))
            
            r= Review.query.get(1234)
            self.assertIsNotNone(r)
 
    def test_search(self):
        """Can logged in user view the advanced search page """
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid
                
            resp = c.get("/search")
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Search by Ingredient", str(resp.data))
            self.assertIn("Search by Category", str(resp.data))
           
    def test_search_ingredient(self):
        """Does the search by ingredient name request work as expected"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.uid
                
            resp = c.post("/search/ingredient", data={"term":"gin"})
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Search results for gin", str(resp.data))
            

    