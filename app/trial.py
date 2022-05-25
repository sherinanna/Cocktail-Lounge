import requests


response=requests.get('http://www.thecocktaildb.com/api/json/v1/1/search.php',
                  params={'s':"margarita"})


# data = resp.json()
# print(data['drinks'])
# print(resp.status_code)

#  get images
# response=requests.get('http://www.thecocktaildb.com/images/ingredients/gin-Small.png')

# print(response.url)
# data = response.json()
# print(dir(response))
# print(response.content) # this will print the response  data in bytes




# # Lookup full cocktail details by id
# response=requests.get('http://www.thecocktaildb.com/api/json/v1/1/lookup.php',
#                    params={'i':11007})


# data = response.json()
# print(data['drinks'])

# def get_random_cocktails(self):
#         """get a random collection of 12 cocktails to display in the homepage"""
        
#         collection=[]
#         while len(collection)<12:
#             response=requests.get('http://www.thecocktaildb.com/api/json/v1/1/random.php')
#             data=response.json()
#             id=data['drinks'][0]['idDrink']
#             if id in collection:
#                 continue
#             else:
#                 collection.append(id)
#         return collection      
            
            
         <a href="{{ url_for('show_cocktail', cocktail_id=drink.strId) }}"
      >{{ drink.strDrink }}</a
    >
    
    # ########
    # searchnfield using input 
    <div class="search-icon input-group">
    <input
      name="name"
      class="form-control input-field"
      placeholder="Enter a cocktail name"
      id="input-field"
    />
    <span class="fa fa-search icon"></span>
  </div>
#  

@app.route('/cocktails')
def list_searched_cocktails():
    """Page with list of the search results
    Can take a 'name' param in querystring to search drink by name."""
    
    term=request.args.get('name')
    drinks=cocktail.search(term)
    return render_template("show_cocktails.html", drinks=drinks, term=term)
  
  
  
  
 .search-container {
  text-align: center;
  padding: 10px;
  text-decoration: none;
  /* background-image: url("https://blackcdn.blacktailnyc.com/what-absinthe-based-cocktail-did-hemingway-create-.jpg"); */
  background-image: url("https://blackcdn.blacktailnyc.com/what-absinthe-based-cocktail-did-hemingway-create-.jpg");
  background-repeat: no-repeat;
  background-size: 100%;
  min-height: 300px;
}

https://hmhub.in/wp-content/uploads/2018/01/rsz_eclipsecocktails1.jpg 


########################

{% extends 'base.html'%} {% block content%}

{% comment %} <div class="container-fluid"> {% endcomment %}
  <div class="row justify-content-center">
    <div class="col-6 advacnced-search-ingredient">
      <div class="card">
        <img
          class="img-fluid"
          src="https://blackcdn.blacktailnyc.com/what-absinthe-based-cocktail-did-hemingway-create-.jpg"
          class="card-img-top"
          alt="Ingredient search"
        />
      </div>
      <div class="bg-secondary text-center">
        <button class="btn btn-block btn-lg search-header">
          Search by Ingredient
        </button>
      </div>
      <div class="bg-light advanced-search-box">
        <form method="POST" action="/search/ingredient" class="form-group">
          {{ form_i.hidden_tag() }} {% for field in form_i if
          field.widget.input_type != 'hidden' %}
          <div class="form-group">
            {% for error in field.errors %}
            <span class="text-danger">{{ error }}</span>
            {% endfor %} {{ field(placeholder="Enter an ingredient",
            class="form-control") }} {% endfor %}
          </div>

          <div class="search-btn">
            <button class="btn btn-block btn-success">Search</button>
          </div>
        </form>
      </div>
    </div>

    <div class="col-6 advacnced-search-category">
      <div class="card">
        <img
          class="img-fluid"
          src="https://hmhub.in/wp-content/uploads/2018/01/rsz_eclipsecocktails1.jpg "
          class="card-img-top"
          alt="category search"
        />
      </div>
      <div class="bg-secondary text-center">
        <button class="btn btn-block btn-lg search-header">
          Search by Category
        </button>
      </div>
      <div class="bg-light advanced-search-box">
        <form method="POST" action="/search/category" class="form-group">
          {% include "_form.html" %}

          <div class="search-btn">
            <button class="btn btn-block btn-success">Search</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

{% endblock %}

            