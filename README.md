# The Cocktail-Lounge App

https://cocktail-lounge-capstone.herokuapp.com/

![This is an image](/capstone1.png)

##Goal:
A go-to website to search for cocktails, get recipes, curate a list of favorites and much more.

Users: 
Anyone above the age of 18 who is  interested to know more about cocktails. A place for amateurs to search for cocktail recipes, experts to quickly create new drinks with at-hand ingredients, with guidance on the best look for a drink.

Data
API Choice: The Cocktail DB
https://www.thecocktaildb.com/api.php?ref=apilist.fun
The API provides cocktail information by name, ingredients, alcohol level and even glass type.



Database Schema:
The schema will consist of a 
Users  table : id, username, password,age,first_name, last_name
Reviews table: id, title, description,user_id, cocktail_id
Favorites table: id,user_id,cocktail_id


