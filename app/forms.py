from ast import Pass
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,PasswordField,SelectField
from wtforms.validators import InputRequired,Length

class UserForm(FlaskForm):
    """form to create a new user"""
    username=StringField('Username', validators=[InputRequired()])
    password=PasswordField('Password',validators=[InputRequired(),Length(min=6)])
    first_name=StringField('First Name', validators=[InputRequired()])
    last_name=StringField('Last Name', validators=[InputRequired()])
    age=IntegerField('Age',validators=[InputRequired()])
    
       
class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired(),Length(min=1, max=20)])
    password = PasswordField('Password', validators=[Length(min=6, max=40)])
    
class ReviewForm(FlaskForm):
    """Add reviews for drinks"""
    review=StringField('Tell us what you think', validators=[InputRequired()])

class SearchForm(FlaskForm):
    """Search for drinks"""
    term=StringField('Enter a cocktail name', validators=[InputRequired()])
   
class CategorySearchForm(FlaskForm):
    """Search for drinks by category"""
    
    categories=["Select a category","Ordinary Drink","Cocktail","Cocoa","Shot","Beer","Homemade Liqueur","Soft Drink"]
    
    category=SelectField('Select a category', choices=categories,validators=[InputRequired()],default="Select a category")
   
