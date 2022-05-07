import requests


# resp=requests.get('http://www.thecocktaildb.com/api/json/v1/1/search.php',
#                   params={'s':"margarita"})

# data = resp.json()
# print(data['drinks'])


# random drink 
# resp=requests.get('http://www.thecocktaildb.com/api/json/v1/1/random.php')

# data = resp.json()
# print(data['drinks'])
# print(resp.status_code)

#  get images
response=requests.get('http://www.thecocktaildb.com/images/ingredients/gin-Small.png')

print(response.url)
# data = response.json()
# print(dir(response))
# print(response.content) # this will print the response  data in bytes




# # Lookup full cocktail details by id
# response=requests.get('http://www.thecocktaildb.com/api/json/v1/1/lookup.php',
#                    params={'i':11007})


# data = response.json()
# print(data['drinks'])