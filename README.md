COCKTAIL ZONE
https://cocktail-zone.herokuapp.com/
Uses the Cocktail DB API (https://www.thecocktaildb.com/api.php)

App sources cocktail information from the API and provides a frontend where users can easily search by name, ingredient, or starting letter,
in addition to a "random" button. It also provides a simple user account system so the user can save cocktails to their favorites list.

When the app is loaded, it presents the user with buttons for the main search pages: Name, Ingredient, All Cocktails (letter), and Random.

The main structure of the app uses Flask, and uses Flask-SQLAlchemy for the accounts system. Each of the search pages populates its results
by pulling data from the API and updating the page via javascript. 