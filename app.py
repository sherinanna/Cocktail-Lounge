# pip install flask
# pip install flask-sqlalchemy
# pip install flask_debugtoolbar
# pip install psycopg2-binary
# pip install flask-wtf
# pip install requests
# pip install flask-bcrypt

import pdb
import os
import re
from flask import Flask, flash,render_template, request,redirect,session,g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Review, Favorite
from forms import UserForm,ReviewForm,LoginForm,SearchForm,CategorySearchForm
from cocktails import Cocktail

cocktail=Cocktail()
app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///cocktail'))
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'shh')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

CURR_USER_KEY = "curr_user"

connect_db(app)
db.create_all()

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.route('/')
def homepage():
    """Homepage of site: display a random list of cocktails
    and form to search for cocktails"""
    
    form=SearchForm()
    drinks=cocktail.get_random_cocktails()
    
    return render_template('home.html',drinks=drinks,form=form)

@app.route('/signup', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = UserForm()

    if form.validate_on_submit():
        try:
            username = form.username.data
            password = form.password.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            age = form.age.data
            
            if age<18:
                flash("Sorry! Return when you are 18 years and up!", 'danger')
                return redirect('/')

            user = User.signup(username, password, first_name, last_name, age)

            db.session.commit()
            
        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)
        
        session[CURR_USER_KEY] = user.id

        return redirect("/")

    else:
        return render_template("users/signup.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form and handle login. submission"""

    if g.user:
        return redirect("/")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  
        if user:
            session[CURR_USER_KEY] = user.id
            return redirect("/")
        
        flash("Invalid credentials.", 'danger')

    return render_template("users/login.html", form=form)


@app.route("/logout")
def logout():
    """Logout route."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    
    flash("Logout Successful", 'success')
    return redirect("/login")

###########  SEARCH ROUTES #####################
@app.route('/search',methods=["GET"])
def advanced_search():
    """Display the search page """
    
    if not g.user:
        flash("Please login to proceed", "danger")
        return redirect("/")
    
    form=CategorySearchForm()
    form_i=SearchForm()
    
    
    return render_template("search_form.html",form_i=form_i,form=form)


@app.route('/search/name',methods=["POST"])
def search_by_name():
    """Page with results for search by name"""
    
    if not g.user:
        flash("Please login to proceed", "danger")
        return redirect("/")
    
    form=SearchForm()
    if form.validate_on_submit():
        term = form.term.data
        drinks=cocktail.search_by_name(term)
        return render_template("show_cocktails.html", drinks=drinks, term=term)
    
    
@app.route('/search/ingredient',methods=["POST"])
def search_by_ingredient():
    """Page with results for search by ingredient"""
   
    if not g.user:
        flash("Please login to proceed", "danger")
        return redirect("/")
    
    form=SearchForm()
    if form.validate_on_submit():
        term = form.term.data
        drinks=cocktail.search_by_ingredient(term)
        return render_template("show_cocktails.html", drinks=drinks, term=term)
       
    
@app.route('/search/category',methods=["POST"])
def search_by_category():
    """Page with results for search by category"""
    
    if not g.user:
        flash("Please login to proceed", "danger")
        return redirect("/")
    
    form=CategorySearchForm()
    
    if form.validate_on_submit():
        term = form.category.data
        drinks=cocktail.search_by_category(term)
        return render_template("show_cocktails.html", drinks=drinks, term=term)
       
################### COCKTAIL ROUTES #############################
    
@app.route('/cocktails/<int:cocktail_id>')
def show_cocktail(cocktail_id):
    """Show details for a cocktail. Includes recipes and user reviews, if any"""
    favorite=False
    if not g.user:
        flash("Please login to proceed", "danger")
        return redirect("/")
    
    drink=cocktail.get_by_id(cocktail_id)
    ingredients,measurement=cocktail.drink_ingredients(drink)
    
    form=ReviewForm()
    
    user_favorites=[fav.cocktail_id for fav in g.user.favorites]
    if cocktail_id in user_favorites:
        favorite=True
    
    reviews=Review.query.filter_by(cocktail_id=cocktail_id).all()
       
    return render_template('cocktail_detail.html',drink=drink,ingredients=ingredients,measurement=measurement,form=form,favorite=favorite,reviews=reviews)

@app.route('/cocktails/<int:cocktail_id>/favorite', methods=['POST'])
def favorite_drinks(cocktail_id):
    """Toggle saved drinks for a user.
    Save drinks favorited by user to the database and redirect to the list of saved drinks"""
    
    if not g.user:
        flash("Please login to proceed", "danger")
        return redirect("/")
    
    user_favorites=[fav.cocktail_id for fav in g.user.favorites]
    
    
    if cocktail_id in user_favorites:
        curr_fav=Favorite.query.filter_by(cocktail_id=cocktail_id,user_id=g.user.id).first()
        db.session.delete(curr_fav)
        # g.user.favorites = [fav for fav in g.user.favorites if fav!=curr_fav]
    
    else:
        g.user.favorites.append(Favorite(user_id=g.user.id,cocktail_id=cocktail_id))
    
    db.session.commit()
    return redirect(f"/users/{g.user.id}/favorites")

@app.route('/cocktails/<int:cocktail_id>/reviews', methods=['POST'])
def review_drink(cocktail_id):
    """Handle the add review form submission.
    Save the drink reviews to the database and redirect to the drink details page"""
    
    if not g.user:
        flash("Please login to proceed", "danger")
        return redirect("/")
    
    form=ReviewForm()
    
    if form.validate_on_submit():
        review=Review(review=form.review.data,user_id=g.user.id, cocktail_id=cocktail_id)
        db.session.add(review)
        # g.user.reviews.append(review)
       
        db.session.commit()

    return redirect(f"/cocktails/{cocktail_id}")
       
    
##########  USER ROUTES  ################

@app.route('/users/<int:user_id>/favorites')
def user_favorites(user_id):
    """Display the saved drinks for a user"""
    
    user_favorites=[fav.cocktail_id for fav in g.user.favorites]
    drinks=cocktail.get_favorites(user_favorites)
    return render_template("/users/favorites.html",drinks=drinks)

@app.route('/reviews/<int:review_id>/delete', methods=["POST"])
def delete_review(review_id):
    """Delete dink review"""
    
    if not g.user:
        flash("Please login to proceed.", "danger")
        return redirect("/")
    
    review=Review.query.get_or_404(review_id)
    if review.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect(f"/cocktails/{review.cocktail_id}")
    
    db.session.delete(review)
    db.session.commit()
    
    return redirect(f"/cocktails/{review.cocktail_id}")