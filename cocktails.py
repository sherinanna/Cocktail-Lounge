
import requests

class Cocktail():
    
    def get_random_cocktails(self):
        """get a random collection of 9 cocktails to display in the homepage"""
        
        collection=[]
        keys=['idDrink','strDrink','strDrinkThumb']
        while len(collection)<9:
            response=requests.get('http://www.thecocktaildb.com/api/json/v1/1/random.php')
            drink=response.json()['drinks'][0]
            
            drinks_in_collection=[dict['idDrink'] for dict in collection]
            if drink['idDrink'] in drinks_in_collection:
                continue
            else:
                collection.append({x:drink[x] for x in keys})
        return collection    
      
            
    def search_by_name(self,term):
        """Send a request to the API to search for cocktails by name
        Return the list of drinks that match the search term"""
        
            
        response=requests.get('http://www.thecocktaildb.com/api/json/v1/1/search.php',
                  params={'s':term})

        drinks=response.json()['drinks']
        
        return drinks  
    
    def search_by_ingredient(self,term):
        """Send a request to the API to search for cocktails by ingredient
        Return the list of drinks that match the search term"""
        
        try:   
            response=requests.get('http://www.thecocktaildb.com/api/json/v1/1/filter.php',
                  params={'i':term})

            drinks=response.json()['drinks']
            return drinks 
        
        except:
            return False
            
        
    def search_by_category(self,term):
        """Send a request to the API to search for cocktails by category
        Return the list of drinks that match the search category"""
        
        try:   
            response=requests.get('http://www.thecocktaildb.com/api/json/v1/1/filter.php',
                  params={'c':term})

            drinks=response.json()['drinks']
            return drinks 
        
        except:
            return False    
        
        
    def get_by_id(self,id):
        """Send a request to the API to retrieve a cocktail by id
        Return the drink that match the id"""
        
            
        response=requests.get('http://www.thecocktaildb.com/api/json/v1/1/lookup.php',
                  params={'i':id})

        drink=response.json()['drinks'][0]
        
        return drink    
        
    def drink_ingredients(self,drink):
        """identify ingredients and their measurements in each drink recipe
        There are atmost 15 ingredients in the api response"""
        
        ingredients=[]
        measurement=[]
        
        for i in range(1,16):
            if drink[ "strIngredient"+ str(i)]:
                ingredients.append(drink[ "strIngredient"+ str(i)])
                measurement.append(drink[ "strMeasure"+ str(i)])
                
        return ingredients,measurement
        
    def get_favorites(self,favorites):
        """Given a list of favorite drink ids, Send a request to the API to retrieve the details 
        about the drinks"""
        
        drinks=[]
        for id in favorites:
            drink=self.get_by_id(id)
            drinks.append(drink)
        
        return drinks

