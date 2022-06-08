"""Test the function within cockyails.py file"""

# run the file as
# FLASK_ENV=production python -m unittest test_cocktails.py

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
    """Test cocktail function"""

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()
        
        self.u = User.signup("test1", "password", "myname","mylastname",30)
        self.uid = 111
        self.u.id=self.uid
        
        db.session.commit()
        
        self.cocktail=Cocktail()
        
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    
    def test_get_random_cocktails(self):
        
        drinks=self.cocktail.get_random_cocktails()
        self.assertEqual(len(drinks),9)
        self.assertEqual(list(drinks[0].keys()),['idDrink','strDrink','strDrinkThumb'])
        
        
    def test_search_by_name(self):
        term="margarita"
        drinks=self.cocktail.search_by_name(term)
        self.assertIn("Margarita",[drink['strDrink'] for drink in drinks])
        # self.assertIn("Margarita",drinks[0]['strDrink'])
        
    def test_search_by_ingredient(self):
        term="orange"
        drinks=self.cocktail.search_by_ingredient(term)
        self.assertEqual(len(drinks),4)
     
        
    def test_search_by_category(self):
        term="cocoa"
        drinks=self.cocktail.search_by_category(term)
        self.assertEqual(len(drinks),9)
       
    def test_get_by_id(self):
        id=11007
        drink=self.cocktail.get_by_id(id)
        self.assertEqual(drink['idDrink'],"11007") 
        self.assertEqual(drink['strDrink'],"Margarita")   
        self.assertEqual(drink['strAlcoholic'],"Alcoholic")  
    
    
    def test_drink_ingredients(self):
        drink=self.cocktail.get_by_id(11007)
        ingredients,measurement=self.cocktail.drink_ingredients(drink)
        self.assertEqual(len(ingredients),4)
        self.assertEqual(ingredients[0],"Tequila")
        
        