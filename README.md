# The Cocktail-Lounge App

https://cocktail-lounge-capstone.herokuapp.com/

![This is an image](/capstone1.png)

## Goal
A go-to website to search for cocktails, get recipes, curate a list of favorites and much more.

## Users
Anyone above the age of 18 who is  interested to know more about cocktails. A place for amateurs to search for cocktail recipes, experts to quickly create new drinks with at-hand ingredients, with guidance on the best look for a drink.

## Technology
Frontend: HTML,CSS Javascript, Jquery, Bootstrap
Backend: Python, Flask, SQLAlchemy, PostgresSQL

## Data
API Choice: The Cocktail DB
https://www.thecocktaildb.com/api.php?ref=apilist.fun
The API provides cocktail information by name, ingredients, alcohol level and even glass type.

## Database Schema
The schema consist of following three tables:
Users  table : id, username, password,age,first_name, last_name
Reviews table: id, title, description,user_id, cocktail_id
Favorites table: id,user_id,cocktail_id

![This is an image](/DatabaseDiagram.png)

## UserFlow

The website homepage will display a random list of cocktails with images. Users can also view the links to search for cocktails by various categories (search by name,ingredients, and category). The page also displays the login/logout/signup links.

To further access the app,each user will need to sign up and login. Only adults above the age of 18 years will be allowed to signup.Users can see the list of cocktails that match the search criteria  and  link to the individual cocktail page that includes the recipe and user reviews.

Users have the option to favorite drinks which gets saved to the user account and post reviews if interested. 
